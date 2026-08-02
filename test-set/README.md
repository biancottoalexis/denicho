# Jeu de test — Phase 0

Dépose ici les photos d'articles dont tu connais **avec certitude** le verdict réel
(authentique ou contrefait), pour que `run-test-set.py` puisse mesurer le vrai taux
de réussite de la détection (seuil de validation : 85%, voir `docs/roadmap-dev.md`).

## Structure attendue

Un sous-dossier par article, nommé :

```
<marque-en-minuscules-avec-tirets>-<vrai|faux>-<identifiant>
```

Contenant 2 à 4 photos (jpg/png/webp/gif) : logo, étiquette intérieure, coutures,
matière — dans l'idéal les mêmes types de photos que celles guidées dans l'app.

## Exemple

```
test-set/
  stone-island-vrai-01/
    logo.jpg
    etiquette.jpg
    couture.jpg
  stone-island-faux-01/
    logo.jpg
    etiquette.jpg
  nike-vrai-01/
    logo.jpg
    etiquette.jpg
    couture.jpg
  nike-faux-01/
    logo.jpg
    etiquette.jpg
```

## Objectif minimum (voir docs/roadmap-dev.md)

- Au moins **20 articles** au total
- Idéalement **10 authentiques / 10 contrefaits**
- Au moins **2 marques différentes**

## Marques avec un nom composé

Pour les marques dont le nom ne se reconstruit pas simplement en remplaçant les
tirets par des espaces (apostrophe, "&"...), voir `SLUG_OVERRIDES` dans
`run-test-set.py` (ex: dossier `levis-vrai-01` -> marque "levi's"). Ajoute une
entrée si besoin pour une marque qui n'y est pas encore.

## Lancer le test une fois les photos en place

```bash
python run-test-set.py --dir test-set --output rapport-phase0.json
```
