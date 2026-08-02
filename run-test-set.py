#!/usr/bin/env python3
"""
Phase 0 — Validation chiffrée de la détection de contrefaçon (voir docs/roadmap-dev.md,
section "Critères de succès chiffrés").

Appelle test-authenticity.py sur un jeu de test d'articles connus (authentiques et
contrefaits) et calcule le taux de verdicts corrects, pour trancher objectivement si
la Phase 0 est validée (seuil : >= 85%).

Structure attendue du dossier de test :

    test-set/
      stone-island-vrai-01/
        logo.jpg
        etiquette.jpg
        couture.jpg
      stone-island-faux-01/
        ...
      nike-vrai-01/
        ...

Chaque sous-dossier = un article, nommé "<marque-en-minuscules-avec-tirets>-<vrai|faux>-<id>"
et contenant 2 à 4 photos (mêmes formats que test-authenticity.py : jpg/png/webp/gif).
Le slug de marque est reconverti en nom de marque en remplaçant les tirets par des
espaces (ex: "the-north-face" -> "the north face") — voir SLUG_OVERRIDES ci-dessous
pour les marques dont le nom ne s'y prête pas telles quelles (apostrophe, "&"...).

Usage:
    python run-test-set.py --dir test-set
    python run-test-set.py --dir test-set --output rapport-phase0.json
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ANALYZE_SCRIPT = SCRIPT_DIR / "test-authenticity.py"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

# Marques dont le nom ne se reconstruit pas proprement à partir d'un simple
# slug-avec-tirets (apostrophe, "&"...). Clé = slug de dossier, valeur = nom de marque
# tel qu'attendu par BRAND_CHECKLISTS dans test-authenticity.py.
SLUG_OVERRIDES = {
    "levis": "levi's",
    "abercrombie-and-fitch": "abercrombie & fitch",
    "abercrombie-fitch": "abercrombie & fitch",
}

FOLDER_PATTERN = re.compile(r"^(?P<brand_slug>.+)-(?P<label>vrai|faux)-(?P<item_id>.+)$")

VERDICT_FOR_LABEL = {
    "vrai": "authentique_probable",
    "faux": "contrefacon_probable",
}

SEUIL_VALIDATION = 85.0
SEUIL_A_AJUSTER = 60.0


def slug_to_brand(slug: str) -> str:
    return SLUG_OVERRIDES.get(slug, slug.replace("-", " "))


def collect_test_items(test_dir: Path) -> list[dict]:
    items = []
    for entry in sorted(test_dir.iterdir()):
        if not entry.is_dir():
            continue
        match = FOLDER_PATTERN.match(entry.name)
        if not match:
            print(f"[ignoré] {entry.name} : ne correspond pas au format <marque>-<vrai|faux>-<id>", file=sys.stderr)
            continue

        images = sorted(p for p in entry.iterdir() if p.suffix.lower() in IMAGE_EXTENSIONS)
        if not (2 <= len(images) <= 4):
            print(f"[ignoré] {entry.name} : {len(images)} image(s) trouvée(s), il en faut 2 à 4", file=sys.stderr)
            continue

        items.append(
            {
                "nom": entry.name,
                "brand": slug_to_brand(match.group("brand_slug")),
                "label_reel": match.group("label"),
                "verdict_attendu": VERDICT_FOR_LABEL[match.group("label")],
                "images": images,
            }
        )
    return items


def run_one(item: dict, model: str) -> dict:
    cmd = [
        sys.executable,
        str(ANALYZE_SCRIPT),
        "--brand",
        item["brand"],
        "--model",
        model,
        *[str(p) for p in item["images"]],
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)

    if proc.returncode != 0:
        return {"erreur": proc.stderr.strip() or "échec inconnu de test-authenticity.py"}

    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"erreur": f"sortie non-JSON : {proc.stdout[:300]}"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dir", required=True, type=Path, help="Dossier contenant les sous-dossiers d'articles de test")
    parser.add_argument("--model", default="claude-opus-5", help="Modèle Claude à utiliser (défaut: claude-opus-5)")
    parser.add_argument("--output", type=Path, help="Chemin d'un fichier JSON où écrire le rapport complet")
    args = parser.parse_args()

    if not args.dir.is_dir():
        parser.error(f"Dossier introuvable : {args.dir}")
    if not ANALYZE_SCRIPT.is_file():
        parser.error(f"test-authenticity.py introuvable à côté de ce script ({ANALYZE_SCRIPT})")

    items = collect_test_items(args.dir)
    if not items:
        parser.error(f"Aucun article de test valide trouvé dans {args.dir}. Voir la structure attendue dans le docstring du script.")

    print(f"{len(items)} article(s) de test trouvé(s). Lancement des analyses...\n", file=sys.stderr)

    results = []
    correct = 0
    errors = 0
    suspect_count = 0
    total_elapsed = 0.0
    total_cost = 0.0
    cost_known_count = 0

    for i, item in enumerate(items, start=1):
        print(f"[{i}/{len(items)}] {item['nom']} ({item['brand']}, attendu={item['label_reel']})...", file=sys.stderr, end=" ")
        outcome = run_one(item, args.model)

        if "erreur" in outcome:
            errors += 1
            print(f"ERREUR : {outcome['erreur']}", file=sys.stderr)
            results.append({**item_summary(item), "erreur": outcome["erreur"]})
            continue

        verdict = outcome.get("verdict")
        est_correct = verdict == item["verdict_attendu"]
        if est_correct:
            correct += 1
        if verdict == "suspect":
            suspect_count += 1

        meta = outcome.get("_meta", {})
        total_elapsed += meta.get("temps_reponse_secondes", 0) or 0
        cout = meta.get("cout_estime_usd")
        if cout is not None:
            total_cost += cout
            cost_known_count += 1

        print(f"verdict={verdict} score={outcome.get('score_confiance')} -> {'OK' if est_correct else 'FAUX'}", file=sys.stderr)

        results.append(
            {
                **item_summary(item),
                "verdict_obtenu": verdict,
                "score_confiance": outcome.get("score_confiance"),
                "mode": outcome.get("mode"),
                "correct": est_correct,
                "meta": meta,
            }
        )

    evaluable = len(items) - errors
    accuracy = (correct / evaluable * 100) if evaluable else 0.0

    print("\n" + "=" * 60, file=sys.stderr)
    print(f"Articles testés          : {len(items)}", file=sys.stderr)
    print(f"Erreurs techniques       : {errors}", file=sys.stderr)
    print(f"Verdicts corrects        : {correct}/{evaluable} ({accuracy:.1f}%)", file=sys.stderr)
    print(f"  dont verdicts 'suspect' (comptés comme incorrects) : {suspect_count}", file=sys.stderr)
    if evaluable:
        print(f"Temps de réponse moyen   : {total_elapsed / evaluable:.1f}s", file=sys.stderr)
    if cost_known_count:
        print(f"Coût estimé total        : ${total_cost:.4f} ({cost_known_count} appel(s) chiffré(s))", file=sys.stderr)
        print(f"Coût estimé moyen/appel  : ${total_cost / cost_known_count:.4f}", file=sys.stderr)

    if accuracy >= SEUIL_VALIDATION:
        verdict_final = f"VALIDÉ : {accuracy:.1f}% >= {SEUIL_VALIDATION}% — la Phase 0 est un succès, on peut passer en Phase 1."
    elif accuracy >= SEUIL_A_AJUSTER:
        verdict_final = (
            f"À AJUSTER : {accuracy:.1f}% est entre {SEUIL_A_AJUSTER}% et {SEUIL_VALIDATION}% — "
            "ajuster le prompt/la méthodologie de scoring (voir docs/features.md) et retester."
        )
    else:
        verdict_final = (
            f"INSUFFISANT : {accuracy:.1f}% < {SEUIL_A_AJUSTER}% — l'angle détection de contrefaçon "
            "n'est probablement pas assez fiable en l'état, revoir le concept avant de continuer."
        )
    print("=" * 60, file=sys.stderr)
    print(verdict_final, file=sys.stderr)

    report = {
        "resume": {
            "articles_testes": len(items),
            "erreurs_techniques": errors,
            "verdicts_corrects": correct,
            "articles_evaluables": evaluable,
            "taux_reussite_pct": round(accuracy, 1),
            "verdicts_suspect": suspect_count,
            "temps_reponse_moyen_secondes": round(total_elapsed / evaluable, 1) if evaluable else None,
            "cout_estime_total_usd": round(total_cost, 4) if cost_known_count else None,
            "cout_estime_moyen_usd": round(total_cost / cost_known_count, 4) if cost_known_count else None,
            "verdict_phase_0": verdict_final,
        },
        "details": results,
    }

    if args.output:
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nRapport complet écrit dans {args.output}", file=sys.stderr)
    else:
        print("\n" + json.dumps(report, ensure_ascii=False, indent=2))


def item_summary(item: dict) -> dict:
    return {
        "article": item["nom"],
        "marque": item["brand"],
        "verdict_attendu": item["verdict_attendu"],
    }


if __name__ == "__main__":
    main()
