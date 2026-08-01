# Dénicho — Roadmap dev

## Phase 0 — Validation technique (avant tout code produit)
- Tester la détection de contrefaçon sur un échantillon de photos connues (vraies/fausses Stone Island) avec un appel direct à une API vision
- Objectif : savoir si la fiabilité est suffisante pour construire une feature dessus
- Si ça ne marche pas bien sur Stone Island, tester sur une autre marque (Nike ou Ralph Lauren) avant d'abandonner l'angle

## Phase 1 — Setup projet
- Init repo, structure dossiers (voir `coding-rules.md`)
- Setup DB (tables de `database.md`)
- Auth basique utilisateur

## Phase 2 — Détection de contrefaçon (MVP feature phare)
- Formulaire upload photos guidé
- Intégration API vision + prompt structuré, avec deux modes : checklist dédiée (marques prioritaires) ou analyse générique (toutes les autres marques)
- Affichage résultat (score + détail par point), avec mention du mode utilisé (précis vs générique)
- Construire la checklist dédiée en premier sur Stone Island (expertise terrain la plus forte), puis étendre marque par marque selon la demande utilisateurs

## Phase 3 — Estimation prix/marge
- Formulaire article
- Logique de calcul de fourchette de prix (base de données de ventes comparables, même partielle/manuelle au début)
- Affichage résultat

## Phase 4 — Génération d'annonce
- Génération titre/description/prix à partir des données de l'article
- Preview + copier

## Phase 5 — Dashboard
- Vue stock, marge, alertes

## Phase 6 — Beta test
- Toi en premier testeur
- 5-10 revendeurs externes (groupes Facebook/Discord revente)

## Phase 7 — Lancement contenu
- Angle : "j'ai créé un outil qui détecte les fausses Stone Island"
- Format faceless (screen recording + voix), même méthode que ZeroToFirst

Détail des prompts Claude Code pour chaque phase : voir `PROMPTS.md`.
