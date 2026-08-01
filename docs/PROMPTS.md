# Dénicho — PROMPTS (Claude Code, phase par phase)

Copie-colle ces prompts dans Claude Code, un par un, dans l'ordre. Chaque prompt suppose que les docs `PRD-MASTER.md`, `features.md`, `database.md`, `ui.md`, `coding-rules.md` sont accessibles dans le repo (dossier `/docs`).

---

## Phase 0 — Test de faisabilité détection contrefaçon

```
Lis /docs/PRD-MASTER.md et /docs/features.md section 2 (détection de contrefaçon).
Crée un script Python simple (test-authenticity.py) qui :
- prend en entrée le nom d'une marque + 2-3 chemins d'images locales
- appelle l'API Claude (vision) avec un prompt structuré demandant d'analyser l'authenticité d'un vêtement de cette marque à partir de : logo, étiquette, coutures, matière
- si la marque n'a pas de checklist connue, utilise un prompt générique de vérification d'authenticité
- retourne un JSON avec verdict + score + détail par point
Objectif : juste tester la fiabilité sur plusieurs marques différentes (au moins Stone Island + une autre marque), pas construire de produit.
```

## Phase 1 — Setup projet

```
Lis tous les fichiers dans /docs.
Initialise un projet avec : frontend React + Tailwind, backend Node.js/Express, PostgreSQL.
Respecte la structure de dossiers et les conventions définies dans /docs/coding-rules.md.
Crée les tables de la base de données décrites dans /docs/database.md via une migration SQL.
Mets en place une auth basique utilisateur (email + mot de passe, JWT).
```

## Phase 2 — Détection de contrefaçon (MVP)

```
Lis /docs/features.md section 2 et /docs/ui.md.
Construis la feature de détection de contrefaçon, ouverte à toutes les marques :
- formulaire d'upload de 3-4 photos guidées (étiquette, logo, zip, matière) + champ marque (texte libre)
- endpoint backend qui vérifie si la marque a une checklist dédiée dans brand_reference_points, sinon utilise le prompt générique (basé sur le test de phase 0)
- stockage du résultat dans la table authenticity_checks
- affichage frontend du verdict avec badge coloré + détail par point + mention du mode (précis/générique) + disclaimer visible (voir coding-rules.md, le disclaimer doit être renvoyé par le backend)
Pré-remplis la checklist dédiée pour Stone Island uniquement pour ce MVP, le reste des marques passe en mode générique.
```

## Phase 3 — Estimation prix/marge

```
Lis /docs/features.md section 1 et /docs/database.md.
Construis la feature d'estimation prix/marge :
- formulaire article (marque, modèle, taille, état, prix d'achat optionnel)
- logique de calcul de fourchette de prix (si pas encore de source de données réelle, utilise une table brand_reference_points ou une base manuelle temporaire à structurer)
- affichage du résultat avec marge estimée en € et %
```

## Phase 4 — Génération d'annonce

```
Lis /docs/features.md section 3.
Construis la génération d'annonce Vinted :
- à partir des données de l'article (marque, modèle, taille, état, mesures)
- génère titre optimisé SEO, description structurée, prix conseillé (relié à l'estimation de la phase 3)
- affiche un preview avec bouton copier
```

## Phase 5 — Dashboard

```
Lis /docs/features.md section 4 et /docs/ui.md.
Construis le dashboard revendeur : liste des articles avec statut, marge totale et par article, alerte pour les articles en stock depuis plus de X jours (seuil configurable).
```

## Notes générales pour toutes les phases

- Toujours relire le fichier `coding-rules.md` avant de générer du code pour respecter les conventions
- Ne jamais formuler un verdict d'authenticité comme une certitude — toujours "probable" / "score de confiance"
- Committer après chaque phase avec un message clair
