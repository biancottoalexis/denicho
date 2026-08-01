#!/usr/bin/env python3
"""
Phase 0 — Test de faisabilité de la détection de contrefaçon (voir docs/PROMPTS.md).

Usage:
    pip install anthropic
    export ANTHROPIC_API_KEY=...  (ou `ant auth login`)
    python test-authenticity.py --brand "Stone Island" photo_logo.jpg photo_etiquette.jpg photo_couture.jpg

Objectif : script jetable pour tester la fiabilité du modèle vision sur plusieurs
marques (au moins Stone Island + une autre), pas un composant produit.
"""

import argparse
import base64
import json
import mimetypes
import sys
from pathlib import Path

import anthropic

MODEL = "claude-opus-5"

DISCLAIMER = (
    "Cette analyse est une estimation générée par IA à titre indicatif. "
    "Elle ne remplace pas l'expertise d'un professionnel certifié et ne "
    "constitue en aucun cas une garantie d'authenticité ou de contrefaçon."
)

# Checklists dédiées, construites au fur et à mesure (voir features.md section 2).
# Une marque sans entrée ici bascule automatiquement en mode générique.
BRAND_CHECKLISTS = {
    "stone island": [
        "Logo/écusson badge boussole : forme, proportions, qualité de broderie/impression, "
        "cohérence de la police du texte 'STONE ISLAND'",
        "Étiquette intérieure : badge détachable avec code article, référence lot, "
        "instructions d'entretien, qualité d'impression du texte",
        "Coutures : régularité du point, qualité des zips (marque, glissement), "
        "finition des surpiqûres",
        "Matière : grammage et texture du tissu technique, cohérence avec la gamme "
        "annoncée (ex. traitement déperlant, doublure)",
    ],
    "nike": [
        "Logo swoosh : proportions, angle, régularité de la couture ou de l'impression",
        "Étiquette intérieure : numéro RN, instructions d'entretien, qualité "
        "d'impression, éventuelle étiquette holographique",
        "Coutures : régularité, absence de fils qui dépassent, qualité des surpiqûres",
        "Matière : grammage, texture, odeur (une forte odeur de colle est suspecte)",
    ],
    "supreme": [
        "Logo box-logo : police (Futura Heavy Oblique), proportions du rectangle rouge, "
        "épaisseur et régularité des lettres",
        "Étiquette intérieure : qualité d'impression, taille et police du texte, "
        "présence et cohérence de l'étiquette de composition/entretien",
        "Coutures : régularité, qualité des finitions, absence de fils qui dépassent",
        "Matière : grammage du tissu, qualité de la sérigraphie ou de la broderie "
        "(craquelures, débordements de couleur)",
    ],
    "ralph lauren": [
        "Logo joueur de polo : proportions du cheval et du cavalier, qualité et "
        "densité de la broderie, couleurs",
        "Étiquette intérieure : police du texte, qualité d'impression, référence "
        "modèle, étiquette de composition",
        "Coutures : régularité, qualité des boutons (souvent gravés du logo), "
        "finition des poignets et du col",
        "Matière : grammage du piqué de coton (polos), qualité perçue du tissu",
    ],
    "carhartt": [
        "Logo/étiquette 'C' : proportions, qualité de la sérigraphie ou du patch cuir, "
        "cohérence de la police du texte 'CARHARTT'",
        "Étiquette intérieure : police du texte, qualité d'impression, référence "
        "modèle, pays de fabrication cohérent avec la gamme",
        "Coutures : robustesse et régularité (workwear = coutures renforcées), "
        "qualité des rivets/boutons",
        "Matière : grammage et texture du canvas/duck cotton, cohérence avec la "
        "gamme annoncée",
    ],
    "the north face": [
        "Logo 'half dome' : proportions, qualité de la broderie, cohérence de la police",
        "Étiquette intérieure : référence modèle, instructions d'entretien, "
        "étiquette de garantie 'lifetime warranty' si applicable",
        "Coutures : qualité des soudures/coutures étanches (vestes techniques), "
        "qualité des zips (marque, glissement)",
        "Matière : cohérence du tissu technique annoncé (Gore-Tex, ripstop...), "
        "texture et grammage",
    ],
}

GENERIC_CHECKLIST = [
    "Logo : cohérence générale de la police, des proportions et de la qualité "
    "d'exécution (broderie, impression ou gravure)",
    "Étiquette intérieure : qualité d'impression, orthographe, cohérence des "
    "informations avec la marque annoncée",
    "Coutures : régularité des points, qualité de finition, absence de fils "
    "qui dépassent",
    "Matière : qualité perçue du tissu ou du matériau, cohérence avec le "
    "positionnement de la marque",
]

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "marque": {"type": "string"},
        "mode": {
            "type": "string",
            "enum": ["precis", "generique"],
            "description": "precis = checklist dédiée à la marque, generique = analyse générale",
        },
        "verdict": {
            "type": "string",
            "enum": ["authentique_probable", "suspect", "contrefacon_probable"],
        },
        "score_confiance": {
            "type": "integer",
            "description": "Score de confiance de 0 à 100 dans le verdict",
        },
        "points_controle": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "point": {"type": "string"},
                    "observation": {"type": "string"},
                    "score": {
                        "type": "integer",
                        "description": "Score de cohérence de 0 à 100 pour ce point précis",
                    },
                },
                "required": ["point", "observation", "score"],
                "additionalProperties": False,
            },
        },
        "resume": {"type": "string"},
    },
    "required": ["marque", "mode", "verdict", "score_confiance", "points_controle", "resume"],
    "additionalProperties": False,
}


def load_image_block(path: Path) -> dict:
    media_type, _ = mimetypes.guess_type(path.name)
    if media_type not in ("image/jpeg", "image/png", "image/webp", "image/gif"):
        raise ValueError(f"Type d'image non supporté pour {path}: {media_type}")
    data = base64.standard_b64encode(path.read_bytes()).decode("utf-8")
    return {
        "type": "image",
        "source": {"type": "base64", "media_type": media_type, "data": data},
    }


def get_checklist(brand: str) -> tuple[list[str], str]:
    checklist = BRAND_CHECKLISTS.get(brand.strip().lower())
    if checklist:
        return checklist, "precis"
    return GENERIC_CHECKLIST, "generique"


def build_prompt(brand: str, checklist: list[str], mode: str) -> str:
    points = "\n".join(f"- {p}" for p in checklist)
    mode_note = (
        "Cette marque dispose d'une checklist de points de contrôle dédiée : "
        "sois aussi précis que possible sur chaque point."
        if mode == "precis"
        else "Aucune checklist dédiée n'existe encore pour cette marque : "
        "analyse de façon générique et affiche un niveau de confiance plus "
        "prudent qu'avec une checklist dédiée."
    )
    return f"""Tu es un expert en authentification de vêtements de seconde main pour la marque "{brand}".

{mode_note}

Analyse les photos fournies (logo, étiquette intérieure, coutures, matière) et évalue
l'authenticité probable de l'article à partir des points de contrôle suivants :
{points}

Consignes :
- Compare chaque point de contrôle à ce que tu observes sur les photos.
- Attribue un score de cohérence (0-100) par point, et un score de confiance global.
- Choisis un verdict parmi : authentique_probable / suspect / contrefacon_probable.
- N'utilise jamais les mots "garanti" ou "certifié" : reste toujours au conditionnel
  ou en termes de probabilité/score de confiance, jamais de certitude absolue.
- Si une photo ne permet pas d'évaluer un point (floue, absente, hors-sujet), dis-le
  explicitement dans l'observation et baisse le score de ce point en conséquence.
- Réponds uniquement selon le format JSON demandé."""


def analyze(brand: str, image_paths: list[Path], model: str) -> dict:
    checklist, mode = get_checklist(brand)
    prompt = build_prompt(brand, checklist, mode)

    content = [load_image_block(p) for p in image_paths]
    content.append({"type": "text", "text": prompt})

    client = anthropic.Anthropic()
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        output_config={"format": {"type": "json_schema", "schema": RESPONSE_SCHEMA}},
        messages=[{"role": "user", "content": content}],
    )

    if response.stop_reason == "refusal":
        raise RuntimeError(f"Le modèle a refusé la requête (stop_details={response.stop_details}).")

    text = next(b.text for b in response.content if b.type == "text")
    result = json.loads(text)

    # Le disclaimer légal est toujours renvoyé côté backend, jamais laissé au modèle
    # (voir docs/coding-rules.md : "toujours inclure le disclaimer... côté backend").
    result["disclaimer"] = DISCLAIMER
    result["mode"] = mode
    result["marque"] = brand
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--brand", required=True, help="Nom de la marque (ex: 'Stone Island')")
    parser.add_argument("--model", default=MODEL, help=f"Modèle Claude à utiliser (défaut: {MODEL})")
    parser.add_argument(
        "images",
        nargs="+",
        type=Path,
        help="2 à 4 chemins d'images locales (logo, étiquette, coutures, matière)",
    )
    args = parser.parse_args()

    if not (2 <= len(args.images) <= 4):
        parser.error("Fournis entre 2 et 4 images.")
    for path in args.images:
        if not path.is_file():
            parser.error(f"Fichier introuvable : {path}")

    try:
        result = analyze(args.brand, args.images, args.model)
    except Exception as exc:  # noqa: BLE001 — script de test, on veut voir l'erreur brute
        print(json.dumps({"error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
