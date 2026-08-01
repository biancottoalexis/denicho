# Dénicho — Decisions (référentiel unique)

Ce fichier recense toutes les décisions techniques/produit tranchées une fois pour toutes. Objectif : chaque nouvelle session Claude Code doit lire ce fichier en premier et s'y référer, au lieu de re-décider ou re-proposer des alternatives déjà tranchées.

**Règle : si Claude Code hésite entre deux options techniques, la réponse est ici. Si ce n'est pas dans ce fichier, poser la question à Alexis plutôt que d'improviser, et ajouter la décision ici une fois prise.**

## Stack

| Sujet | Décision | Raison |
|---|---|---|
| Backend | FastAPI (Python) | Logique vision au cœur du produit, un seul langage backend |
| Frontend | React + Tailwind | Cohérent avec ZeroToFirst |
| DB | PostgreSQL | Standard, bon support relations + JSONB |
| Librairie composants | shadcn/ui | Évite de réinventer un design system à chaque session |
| Hébergement backend + DB | Railway | Simple, pas cher, bon support Python/Postgres |
| Hébergement frontend | Vercel | Standard pour React |
| Paiement | Stripe | Standard abonnements SaaS |
| Vision/IA | API Claude (vision) | Déjà choisi dès le PRD initial |
| Tests | pytest | Cohérent avec FastAPI |

## Produit

| Sujet | Décision | Raison |
|---|---|---|
| Détection auto de marque par photo | Non en V1, saisie manuelle uniquement | Réduit le risque technique de la Phase 0, pas la priorité |
| Source de données prix V1 | Base manuelle + eBay API | Scraping Vinted non validé légalement, voir `legal.md` |
| Seuils de verdict authenticité | ≥75 authentique / 40-74 suspect / <40 contrefaçon | Hypothèse de départ, à ajuster après Phase 0 |
| Scope marques détection contrefaçon | Toutes marques (checklist dédiée si dispo, sinon générique) | Décision utilisateur du 02/08/2026 |
| Nom du produit | Dénicho | Validé, dispo vérifiée à l'oral, à confirmer .fr/.com |

## Historique des changements

- 02/08/2026 : passage de "4 marques prioritaires" à "toutes les marques" pour la détection de contrefaçon
- 02/08/2026 : ajout de ce fichier suite à une revue de gaps sur la documentation initiale
