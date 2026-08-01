# Dénicho — Coding rules

## Stack

- Frontend : React + Tailwind
- Backend : Node.js/Express (ou FastAPI si logique vision plus lourde côté Python)
- DB : PostgreSQL
- Vision/IA : API multimodale (Claude) pour l'analyse des photos de contrefaçon

## Règles générales

- Composants React : un fichier par composant, nommage PascalCase
- Pas de logique métier dans les composants UI — tout passe par des services/API
- Toute réponse liée à la détection de contrefaçon doit systématiquement inclure le disclaimer légal côté backend (pas seulement affiché côté frontend) — ne jamais renvoyer un verdict sans ce champ
- Jamais de terme "garanti" ou "certifié" dans les textes générés ou codés en dur — toujours "score de confiance", "probable", "indicatif"

## Structure de dossiers recommandée

```
/src
  /components
  /pages
  /services       → appels API (estimation, authenticity-check, listing-generation)
  /hooks
/server
  /routes
  /services       → logique métier (scoring, appel API vision, génération annonce)
  /db
```

## Conventions API

- Toutes les routes retournent un objet `{ success, data, error }`
- Les endpoints liés à l'IA (estimation, détection contrefaçon, génération annonce) doivent logger le prompt et la réponse brute pour debug/amélioration continue

## Sécurité / légal

- Ne jamais stocker les photos utilisateur sans consentement explicite affiché
- Prévoir mentions légales dédiées pour la fonctionnalité détection de contrefaçon (voir `vision.md` section "Ce que Dénicho n'est PAS")
