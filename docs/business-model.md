# Dénicho — Business Model

## Structure de pricing

### Free
- 3 estimations prix/marge par mois
- 1 détection de contrefaçon par mois
- Pas de génération d'annonce
- Objectif : faire tester la feature phare (contrefaçon) pour convertir

### Starter — 9€/mois
- Estimations illimitées
- 10 détections de contrefaçon/mois
- Génération d'annonce illimitée
- Dashboard basique

### Pro — 19€/mois
- Tout illimité (estimations, détections contrefaçon, annonces)
- Dashboard avancé (alertes stock, export CSV)
- Accès prioritaire aux nouvelles marques ajoutées à la détection

## Pourquoi ce découpage

La détection de contrefaçon est le produit d'appel (feature qu'aucun concurrent n'a) mais aussi le plus coûteux à fournir (appels API vision) → elle est limitée en Free et Starter, illimitée seulement en Pro. Ça pousse naturellement vers l'upsell.

## Coûts variables à surveiller

- Coût par appel API vision (détection contrefaçon) — à calculer précisément en Phase 0 avant de fixer les prix définitifs
- Coût de scraping/mise à jour des données de vente comparables

## Acquisition — coût zéro au départ

- Contenu faceless (screen recording + voix), même méthode que ZeroToFirst
- Groupes Facebook/Discord de revendeurs Vinted comme canal beta gratuit
- Pas de budget pub prévu en V1

## Métriques clés à suivre dès le lancement

- Taux de conversion Free → payant
- Nombre de détections de contrefaçon par utilisateur/mois (indicateur d'engagement sur la feature phare)
- Churn mensuel
- Coût API moyen par utilisateur payant (marge réelle)
