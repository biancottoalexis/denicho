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
    "adidas": [
        "Logo trèfle ou 3 bandes : régularité de l'espacement et de l'angle des "
        "bandes, qualité de l'impression ou de la broderie",
        "Étiquette intérieure : référence article, tampon 'adidas AG', pays de "
        "fabrication cohérent, instructions d'entretien",
        "Coutures : régularité, qualité des surpiqûres sur les bandes latérales",
        "Matière : grammage et texture, cohérence avec la technologie technique "
        "annoncée (ex. Primeknit, Climacool)",
    ],
    "puma": [
        "Logo puma bondissant : proportions, netteté du contour, qualité de la "
        "broderie ou de l'impression",
        "Étiquette intérieure : police du texte 'PUMA', référence modèle, "
        "instructions d'entretien",
        "Coutures : régularité, qualité des finitions sur les bandes latérales",
        "Matière : grammage, texture, cohérence avec la gamme technique annoncée",
    ],
    "new balance": [
        "Logo 'N' : symétrie, épaisseur régulière, qualité de la couture/broderie "
        "sur les côtés (souvent cousu, pas simplement collé sur les modèles premium)",
        "Étiquette intérieure : référence modèle, cohérence 'Made in USA/UK' "
        "avec la gamme, instructions d'entretien",
        "Coutures : qualité et régularité, finition des empiècements",
        "Matière : qualité du daim/mesh, grammage",
    ],
    "under armour": [
        "Logo 'UA' entrelacé : netteté, régularité des lignes",
        "Étiquette intérieure : police du texte, référence modèle, technologie "
        "annoncée (HeatGear, ColdGear...) cohérente",
        "Coutures : qualité des surpiqûres techniques, régularité",
        "Matière : texture technique (compression, mesh), grammage",
    ],
    "reebok": [
        "Logo vector/delta : proportions, qualité de l'impression ou de la broderie",
        "Étiquette intérieure : police du texte 'Reebok', référence modèle, "
        "instructions d'entretien",
        "Coutures : régularité, qualité des finitions",
        "Matière : grammage, texture",
    ],
    "converse": [
        "Patch cheville (étoile bleue) : netteté de l'impression, régularité de "
        "l'étoile et du texte 'Chuck Taylor All Star'",
        "Étiquette semelle intérieure : référence, taille, mentions 'All Star'",
        "Coutures : qualité de la toile, régularité des points sur la semelle "
        "en caoutchouc",
        "Matière : toile canvas (grammage), semelle caoutchouc (texture, odeur)",
    ],
    "vans": [
        "Logo 'V' latéral (patch ou étiquette) : netteté, position exacte sur le côté",
        "Étiquette languette : référence modèle, taille, mention 'off the wall'",
        "Coutures : qualité de la jonction toile/semelle, régularité",
        "Matière : toile, semelle caoutchouc gaufrée (motif waffle régulier)",
    ],
    "fila": [
        "Logo 'F' encadré : proportions, qualité de l'impression",
        "Étiquette intérieure : police du texte, référence, instructions d'entretien",
        "Coutures : régularité",
        "Matière : grammage, texture",
    ],
    "champion": [
        "Logo 'C' brodé sur la manche : régularité de la broderie, proportions",
        "Étiquette intérieure : police 'Champion', mention 'Reverse Weave' si "
        "applicable, instructions d'entretien",
        "Coutures : régularité, qualité des surpiqûres",
        "Matière : grammage du molleton, tissage particulier du 'Reverse Weave' "
        "(résistance au rétrécissement)",
    ],
    "lacoste": [
        "Logo crocodile brodé : proportions, densité de la broderie, cohérence "
        "de la couleur verte",
        "Étiquette intérieure : police du texte, référence, petit crocodile sur "
        "l'étiquette, instructions d'entretien",
        "Coutures : qualité du col piqué, boutons (souvent gravés du logo)",
        "Matière : grammage du piqué de coton",
    ],
    "tommy hilfiger": [
        "Logo drapeau : proportions, netteté des couleurs (rouge/blanc/bleu)",
        "Étiquette intérieure : police du texte, référence, instructions d'entretien",
        "Coutures : régularité",
        "Matière : grammage, texture",
    ],
    "calvin klein": [
        "Logo/bandeau élastique 'Calvin Klein' (sous-vêtements) ou étiquette "
        "texte minimaliste : régularité de l'impression, police exacte",
        "Étiquette intérieure : référence, instructions d'entretien, composition "
        "matière indiquée",
        "Coutures : régularité",
        "Matière : grammage",
    ],
    "levi's": [
        "Étiquette rouge poche arrière 'Levi's' : police exacte, forme régulière",
        "Étiquette taille/entretien intérieure et patch cuir '2 chevaux' au dos",
        "Coutures : fil orange caractéristique, rivets cuivrés, qualité des surpiqûres",
        "Matière : denim (poids, texture, cohérence du délavage)",
    ],
    "diesel": [
        "Patch cuir arrière (jeans) : qualité de la gravure, police",
        "Étiquette intérieure : référence modèle, instructions d'entretien",
        "Coutures : qualité, rivets",
        "Matière : denim/tissu, grammage",
    ],
    "guess": [
        "Logo triangle : proportions, netteté",
        "Étiquette intérieure : police du texte, référence, instructions d'entretien",
        "Coutures : régularité",
        "Matière : grammage, texture",
    ],
    "patagonia": [
        "Logo montagne brodé/imprimé : netteté des couleurs, proportions",
        "Étiquette intérieure : référence, cohérence de la matière technique "
        "annoncée (souvent recyclée), instructions d'entretien",
        "Coutures : qualité d'étanchéité (vestes techniques)",
        "Matière : tissu technique annoncé, grammage",
    ],
    "columbia": [
        "Logo cercle 'Columbia' : netteté, proportions",
        "Étiquette intérieure : référence, cohérence de la technologie annoncée "
        "(Omni-Heat, Omni-Tech...), instructions d'entretien",
        "Coutures : qualité, étanchéité",
        "Matière : texture technique cohérente",
    ],
    "dickies": [
        "Logo/étiquette rectangulaire rouge : police, netteté",
        "Étiquette intérieure : référence modèle (ex. '874'), instructions d'entretien",
        "Coutures : robustesse workwear, régularité, double surpiqûre",
        "Matière : grammage du twill",
    ],
    "timberland": [
        "Logo arbre : netteté, proportions, broderie ou gravure cuir",
        "Étiquette intérieure : référence modèle, instructions d'entretien",
        "Coutures : qualité des coutures cuir (souvent Goodyear welt sur les "
        "modèles premium)",
        "Matière : qualité du cuir nubuck, semelle caoutchouc",
    ],
    "burberry": [
        "Motif tartan check : régularité et alignement des lignes et des "
        "couleurs (beige, noir, rouge, blanc), qualité du tissage/impression",
        "Étiquette intérieure : police, référence, cohérence 'Made in England/Italy'",
        "Coutures : finition haut de gamme, régularité",
        "Matière : grammage et texture du coton gabardine",
    ],
    "gucci": [
        "Motif double G / GG : symétrie, netteté, régularité de la répétition du motif",
        "Étiquette intérieure : police, numéro de série, instructions d'entretien, "
        "cohérence 'Made in Italy'",
        "Coutures : finition haut de gamme, régularité",
        "Matière : qualité perçue du cuir ou du tissu",
    ],
    "louis vuitton": [
        "Motif monogramme (LV) : alignement et symétrie du motif, netteté des "
        "contours, régularité de la répétition",
        "Étiquette intérieure : numéro de date (date code), police, cohérence "
        "'Made in France/Italy/USA'",
        "Coutures : finition haut de gamme, régularité (généralement très dense "
        "sur le cuir naturel)",
        "Matière : qualité du canvas enduit ou du cuir naturel (odeur, patine)",
    ],
    "chanel": [
        "Logo double C : symétrie parfaite, proportions, netteté de la gravure "
        "ou de la broderie",
        "Étiquette intérieure : numéro de série, police, cohérence 'Made in "
        "France/Italy'",
        "Coutures : finition haut de gamme, régularité extrême",
        "Matière : qualité du tweed ou du cuir matelassé, poids",
    ],
    "dior": [
        "Logo 'CD' ou motif oblique : netteté, symétrie, régularité",
        "Étiquette intérieure : référence, numéro de série, police, cohérence "
        "'Made in Italy/France'",
        "Coutures : finition haut de gamme, régularité",
        "Matière : qualité perçue du tissu ou du cuir",
    ],
    "prada": [
        "Triangle logo métallique : netteté de la gravure, fixation régulière",
        "Étiquette intérieure : police, numéro de série, cohérence 'Made in Italy'",
        "Coutures : finition haut de gamme, régularité",
        "Matière : qualité du nylon technique (Re-Nylon) ou du cuir saffiano "
        "(grain régulier)",
    ],
    "balenciaga": [
        "Logo texte imprimé : police exacte, netteté de l'impression",
        "Étiquette intérieure : référence, instructions d'entretien, cohérence "
        "'Made in Italy'",
        "Coutures : finition, régularité",
        "Matière : grammage, texture (souvent oversized ou technique)",
    ],
    "versace": [
        "Logo Méduse : netteté du détail, proportions, dorure régulière",
        "Étiquette intérieure : police, référence, cohérence 'Made in Italy'",
        "Coutures : finition haut de gamme",
        "Matière : qualité de la soie ou du coton, précision des motifs baroques",
    ],
    "armani": [
        "Logo aigle (Emporio Armani) ou texte : netteté, proportions",
        "Étiquette intérieure : police, référence, cohérence 'Made in Italy'",
        "Coutures : finition, régularité",
        "Matière : qualité perçue, grammage",
    ],
    "hugo boss": [
        "Logo/texte 'BOSS' : police exacte, netteté",
        "Étiquette intérieure : référence, instructions d'entretien",
        "Coutures : régularité, finition",
        "Matière : grammage, texture",
    ],
    "moncler": [
        "Patch tricolore (bleu/blanc/rouge) avec coq : netteté, proportions, "
        "fixation régulière",
        "Étiquette intérieure : numéro de série, police, cohérence 'Made in...', "
        "certification du duvet",
        "Coutures : qualité des surpiqûres de caissons (baffles), étanchéité",
        "Matière : qualité du duvet (gonflant), tissu extérieur",
    ],
    "canada goose": [
        "Patch écusson rond (arctic) : netteté, couleurs, fixation",
        "Étiquette intérieure : numéro de série, instructions d'entretien, "
        "hologramme d'authenticité si présent",
        "Coutures : qualité des caissons, étanchéité",
        "Matière : duvet, tissu Arctic-Tech",
    ],
    "off-white": [
        "Logo flèches / texte 'OFF-WHITE' : police Helvetica caractéristique, "
        "netteté de l'impression, guillemets caractéristiques",
        "Étiquette intérieure : référence, instructions d'entretien",
        "Coutures : régularité",
        "Matière : grammage, texture",
    ],
    "palm angels": [
        "Logo ours / texte : police, netteté de l'impression",
        "Étiquette intérieure : référence, instructions d'entretien",
        "Coutures : régularité",
        "Matière : grammage",
    ],
    "bape": [
        "Motif camouflage caractéristique et logo tête de singe : netteté et "
        "régularité du motif, précision du logo brodé",
        "Étiquette intérieure : référence, instructions d'entretien, tag "
        "'A Bathing Ape'",
        "Coutures : régularité, qualité",
        "Matière : grammage du molleton, qualité du print camouflage",
    ],
    "stussy": [
        "Logo signature manuscrite : fluidité et régularité du tracé (imprimé "
        "ou brodé), proportions",
        "Étiquette intérieure : référence, instructions d'entretien",
        "Coutures : régularité",
        "Matière : grammage",
    ],
    "palace": [
        "Logo tri-ferg (triangle) : netteté, proportions, régularité des trois segments",
        "Étiquette intérieure : référence, instructions d'entretien",
        "Coutures : régularité",
        "Matière : grammage",
    ],
    "kenzo": [
        "Logo tigre brodé : densité et précision de la broderie, cohérence des couleurs",
        "Étiquette intérieure : référence, instructions d'entretien, cohérence "
        "'Made in...'",
        "Coutures : finition",
        "Matière : grammage, qualité du molleton ou du tissu",
    ],
    "fred perry": [
        "Logo laurier brodé sur la poitrine : proportions, précision de la broderie",
        "Étiquette intérieure : référence, instructions d'entretien, liseré "
        "caractéristique sur col/manches",
        "Coutures : régularité, qualité du col piqué",
        "Matière : grammage du piqué de coton",
    ],
    "nautica": [
        "Logo drapeau/voile : netteté, proportions",
        "Étiquette intérieure : référence, instructions d'entretien",
        "Coutures : régularité",
        "Matière : grammage",
    ],
    "abercrombie & fitch": [
        "Logo élan brodé : précision de la broderie, proportions",
        "Étiquette intérieure : référence, instructions d'entretien",
        "Coutures : régularité",
        "Matière : grammage, qualité du coton",
    ],
    "hollister": [
        "Logo mouette/texte : précision, netteté",
        "Étiquette intérieure : référence, instructions d'entretien",
        "Coutures : régularité",
        "Matière : grammage",
    ],
    "saint laurent": [
        "Logo monogramme YSL : netteté, proportions, précision de la gravure "
        "ou de l'impression",
        "Étiquette intérieure : référence, numéro de série, cohérence 'Made in Italy'",
        "Coutures : finition haut de gamme",
        "Matière : qualité perçue du tissu ou du cuir",
    ],
    "givenchy": [
        "Logo texte 'GIVENCHY' ou motif 4G : netteté, régularité",
        "Étiquette intérieure : référence, numéro de série, cohérence 'Made in Italy'",
        "Coutures : finition haut de gamme",
        "Matière : qualité perçue du tissu ou du cuir",
    ],
    "jordan": [
        "Logo Jumpman : silhouette précise, proportions, netteté",
        "Étiquette languette/intérieure : référence modèle (colorway), taille, "
        "tag 'Nike Air'",
        "Coutures : qualité, régularité des surpiqûres",
        "Matière : cuir/mesh, semelle (poids, rebond, odeur de colle suspecte)",
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
