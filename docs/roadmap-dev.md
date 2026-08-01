# Dénicho — Roadmap dev

## Phase 0 — Validation technique (avant tout code produit)
- Tester la détection de contrefaçon sur un échantillon de photos connues (vraies/fausses Stone Island + au moins une autre marque) avec un appel direct à une API vision
- Objectif : savoir si la fiabilité est suffisante pour construire une feature dessus
- Si ça ne marche pas bien sur Stone Island, tester sur une autre marque (Nike ou Ralph Lauren) avant d'abandonner l'angle

### Critères de succès chiffrés (obligatoires pour valider la Phase 0)

- Construire un jeu de test d'au moins **20 articles connus** (authentiques et contrefaits mélangés, idéalement 10/10) sur au moins 2 marques
- Faire tourner `test-authenticity.py` sur chaque article et comparer le verdict retourné à la réalité connue
- **Seuil de validation : ≥ 85% de verdicts corrects** sur ce jeu de test
- Si le taux est en dessous de 85% :
  - Entre 60% et 85% : ajuster le prompt/la méthodologie de scoring (voir `features.md`) et retester avant d'abandonner
  - En dessous de 60% : l'angle détection de contrefaçon n'est probablement pas assez fiable en l'état, revoir le concept avec Alexis avant de continuer le développement
- Noter également le coût réel mesuré par appel (à reporter dans `business-model.md`) et le temps de réponse moyen (pour la stratégie de timeout dans `coding-rules.md`)
- Cette validation ne se discute pas au feeling — le chiffre tranche

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
