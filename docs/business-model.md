# Dénicho — Business Model

## Processeur de paiement

Stripe — décision tranchée (voir `coding-rules.md` et `decisions.md`). Gère abonnements récurrents, essais gratuits, et webhooks pour synchroniser la table `subscriptions`.

## Structure de pricing

**Important : ce pricing est une hypothèse de travail, pas définitif.** Il doit être confirmé/ajusté une fois le coût réel mesuré en Phase 0 (voir section "Coûts variables" ci-dessous). Ne pas communiquer publiquement ces prix avant cette validation.

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

- **Coût par appel API vision (détection contrefaçon)** — à mesurer précisément pendant la Phase 0 : noter le coût réel en tokens/€ pour chaque appel du script `test-authenticity.py` (nombre d'images envoyées, taille des prompts) et l'extrapoler sur le volume mensuel attendu par plan (ex : 10 détections/mois en Starter). Ce chiffre doit être reporté ici une fois connu, avant de figer les prix.
- Coût de mise à jour de la base manuelle de prix (Feature 1) — temps humain au démarrage, pas de coût scraping tant que ce point n'est pas validé légalement (voir `legal.md`)

## Acquisition — coût zéro au départ

- Contenu faceless (screen recording + voix), même méthode que ZeroToFirst
- Groupes Facebook/Discord de revendeurs Vinted comme canal beta gratuit
- Pas de budget pub prévu en V1

## Métriques clés à suivre dès le lancement

- Taux de conversion Free → payant
- Nombre de détections de contrefaçon par utilisateur/mois (indicateur d'engagement sur la feature phare)
- Churn mensuel
- Coût API moyen par utilisateur payant (marge réelle)
