# Dénicho — Coding rules

## Stack (tranchée, ne pas réouvrir la discussion)

- Frontend : React + Tailwind
- Backend : **FastAPI (Python)** — décision définitive, pas Node/Express. Raison : la logique vision (cœur du produit) est plus naturelle en Python, et un seul langage backend pour tout (API + appels vision + scoring) évite de dupliquer la logique dans deux écosystèmes
- DB : PostgreSQL
- Vision/IA : API Claude (vision) pour l'analyse des photos de contrefaçon
- Paiement : Stripe (voir `business-model.md`)
- Hébergement : **Railway** pour backend + DB (simple, pas cher, bon support Python/Postgres), **Vercel** pour le frontend React. À réévaluer seulement si la charge explose (migration VPS/AWS envisageable en V2+)

Toute décision technique supplémentaire (nouvelle lib, nouveau service tiers) doit être ajoutée à `decisions.md`, pas improvisée en cours de session Claude Code.

## Secrets & configuration

- Clé API Anthropic, credentials DB, clé Stripe : dans `.env` en local, jamais commité (`.env` dans `.gitignore` dès le premier commit)
- En prod : variables d'environnement gérées directement par Railway/Vercel (pas de secret manager externe nécessaire au stade MVP)
- Un fichier `.env.example` doit lister toutes les variables attendues sans valeurs réelles

## Stratégie de retry / timeout / fallback (appel API vision)

- Timeout appel API vision : 30 secondes max
- En cas de timeout ou d'erreur : 1 retry automatique, puis si échec persistant → retourner à l'utilisateur un statut clair "analyse indisponible, réessayez" (jamais un verdict par défaut inventé)
- Si l'API refuse la requête (contenu bloqué, image illisible) : retourner un message explicite à l'utilisateur, ne jamais masquer l'erreur derrière un score neutre

## Convention de tests

- Tests obligatoires minimum :
  - Le calcul de scoring d'authenticité (agrégation des points → score global → verdict) : tests unitaires sur les seuils (voir `features.md`)
  - Les endpoints critiques : `POST /items/:id/authenticity-check`, `POST /items/:id/estimate`, `POST /items/:id/generate-listing`
  - Le calcul de marge (prix vente estimé - prix achat)
- Framework : pytest (cohérent avec FastAPI)
- Aucune Phase de `roadmap-dev.md` n'est considérée terminée sans ces tests passants

## Règles générales

- Composants React : un fichier par composant, nommage PascalCase
- Pas de logique métier dans les composants UI — tout passe par des services/API
- Toute réponse liée à la détection de contrefaçon doit systématiquement inclure le disclaimer légal côté backend (pas seulement affiché côté frontend) — ne jamais renvoyer un verdict sans ce champ
- Jamais de terme "garanti" ou "certifié" dans les textes générés ou codés en dur — toujours "score de confiance", "probable", "indicatif"

## Structure de dossiers recommandée

```
/src                → frontend React
  /components
  /pages
  /services         → appels API (estimation, authenticity-check, listing-generation)
  /hooks
/server              → backend FastAPI
  /routers           → endpoints (items, estimate, authenticity, listings, dashboard)
  /services          → logique métier (scoring, appel API vision, génération annonce)
  /models            → modèles Pydantic + ORM (SQLAlchemy)
  /db                → migrations et connexion DB
/tests               → tests pytest
```

## Conventions API

- Toutes les routes retournent un objet `{ success, data, error }`
- Les endpoints liés à l'IA (estimation, détection contrefaçon, génération annonce) doivent logger le prompt et la réponse brute pour debug/amélioration continue

## Sécurité / légal

- Ne jamais stocker les photos utilisateur sans consentement explicite affiché
- Prévoir mentions légales dédiées pour la fonctionnalité détection de contrefaçon (voir `vision.md` section "Ce que Dénicho n'est PAS")
