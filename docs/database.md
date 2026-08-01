# Dénicho — Database

## Stack
PostgreSQL

## Tables

### users
| Colonne | Type | Notes |
|---|---|---|
| id | uuid | PK |
| email | text | unique |
| plan | text | free / premium |
| created_at | timestamp | |

### items
| Colonne | Type | Notes |
|---|---|---|
| id | uuid | PK |
| user_id | uuid | FK users |
| marque | text | |
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
| marque | text | |
| type_point_controle | text | logo / etiquette / couture / zip / matiere |
| description | text | ce qu'il faut vérifier pour ce point |

## Notes d'implémentation

- `details_json` doit stocker un objet structuré du type :
```json
{
  "logo": {"verdict": "coherent", "confiance": 82},
  "etiquette": {"verdict": "suspecte", "confiance": 40, "raison": "police de caractère non conforme"}
}
```
- Prévoir un index sur `items.user_id` et `items.statut` pour les requêtes dashboard
