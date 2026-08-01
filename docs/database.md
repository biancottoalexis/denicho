# Dénicho — Database

## Stack
PostgreSQL

## Tables

### users
| Colonne | Type | Notes |
|---|---|---|
| id | uuid | PK |
| email | text | unique |
| password_hash | text | bcrypt/argon2, jamais le mot de passe en clair |
| refresh_token | text | nullable, pour l'auth JWT (Phase 1) |
| plan | text | free / starter / pro (voir `subscriptions` pour le détail Stripe) |
| consent_given_at | timestamp | nullable, date de consentement RGPD explicite avant tout upload photo |
| created_at | timestamp | |

### subscriptions
| Colonne | Type | Notes |
|---|---|---|
| id | uuid | PK |
| user_id | uuid | FK users |
| stripe_customer_id | text | |
| stripe_subscription_id | text | nullable si free |
| plan | text | free / starter / pro |
| statut | text | active / annule / impaye |
| date_renouvellement | timestamp | nullable |

### brands
| Colonne | Type | Notes |
|---|---|---|
| id | uuid | PK |
| slug | text | unique, format canonique en minuscule (ex: "stone-island") |
| nom_affichage | text | ex: "Stone Island" |

### items
| Colonne | Type | Notes |
|---|---|---|
| id | uuid | PK |
| user_id | uuid | FK users |
| brand_id | uuid | FK brands (remplace le champ texte libre "marque" pour éviter les doublons Nike/nike/NIKE) |
| modele | text | |
| taille | text | |
| etat | text | neuf/tres_bon/bon/satisfaisant |
| prix_achat | numeric | nullable |
| prix_vente_estime_min | numeric | |
| prix_vente_estime_max | numeric | |
| statut | text | en_stock / en_vente / vendu |
| created_at | timestamp | |

### item_photos
| Colonne | Type | Notes |
|---|---|---|
| id | uuid | PK |
| item_id | uuid | FK items |
| url | text | |
| type | text | etiquette / logo / couture / global |
| supprimer_apres | timestamp | date de purge automatique (voir politique de rétention ci-dessous) |

### authenticity_checks
| Colonne | Type | Notes |
|---|---|---|
| id | uuid | PK |
| item_id | uuid | FK items |
| score | numeric | 0-100 |
| verdict | text | authentique_probable / suspect / contrefacon_probable |
| details_json | jsonb | détail par point de contrôle |
| created_at | timestamp | |

### listings
| Colonne | Type | Notes |
|---|---|---|
| id | uuid | PK |
| item_id | uuid | FK items |
| titre_genere | text | |
| description_generee | text | |
| prix_conseille | numeric | |
| publie | boolean | default false |

### brand_reference_points
| Colonne | Type | Notes |
|---|---|---|
| id | uuid | PK |
| brand_id | uuid | FK brands |
| type_point_controle | text | logo / etiquette / couture / zip / matiere |
| description | text | ce qu'il faut vérifier pour ce point |

### authenticity_feedback
| Colonne | Type | Notes |
|---|---|---|
| id | uuid | PK |
| authenticity_check_id | uuid | FK authenticity_checks |
| user_id | uuid | FK users |
| feedback | text | "verdict_correct" / "verdict_incorrect" |
| commentaire | text | nullable, précision libre de l'utilisateur |
| created_at | timestamp | |

Cette table alimente l'enrichissement de `brand_reference_points` dans le temps (voir `vision.md` — différenciateur long terme).

## Politique de rétention des photos

- Les photos uploadées pour la détection de contrefaçon sont conservées **90 jours** après l'analyse, puis purgées automatiquement (job cron quotidien qui supprime les fichiers dont `item_photos.supprimer_apres` est dépassé)
- L'utilisateur peut demander une suppression immédiate à tout moment (conformité RGPD)

## Notes d'implémentation

- `details_json` doit stocker un objet structuré du type :
```json
{
  "logo": {"verdict": "coherent", "confiance": 82},
  "etiquette": {"verdict": "suspecte", "confiance": 40, "raison": "police de caractère non conforme"}
}
```
- Prévoir un index sur `items.user_id` et `items.statut` pour les requêtes dashboard
