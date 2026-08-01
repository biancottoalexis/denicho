# Dénicho — PRD MASTER

## 1. Vision produit

Dénicho aide les revendeurs de vêtements seconde main (Vinted, eBay, friperies) à acheter et revendre en confiance :
- Savoir si un article vaut le coup avant de l'acheter (estimation prix de revente + marge)
- Détecter si un article est probablement contrefait
- Générer une annonce Vinted optimisée en 30 secondes
- Suivre stock et marges dans un dashboard

## 2. Problème

- Achats à l'instinct sans données fiables → mauvaises marges
- Contrefaçons (Stone Island, Nike, Supreme...) → perte sèche, bannissement Vinted, ou pire, revente involontaire de contrefaçon
- Rédaction d'annonce chronophage et mal optimisée pour l'algo Vinted

## 3. Cible

Revendeurs Vinted/eBay débutants à intermédiaires (0 à 500 ventes/mois), profil streetwear/vintage premium (Stone Island, Supreme, Carhartt, Ralph Lauren, The North Face) — le profil BCT_Store.

## 4. Proposition de valeur unique

Aucun concurrent (ControlResell, Flippd, TrendResell, Friptadium, ResellVinted) ne fait de détection de contrefaçon. C'est l'angle d'entrée : la confiance sur l'authenticité avant même la marge ou l'automatisation.

## 5. Fonctionnalités V1

Voir `features.md` pour le détail complet.
1. Estimation prix & marge
2. Détection de contrefaçon (feature phare)
3. Génération d'annonce
4. Dashboard revendeur

## 6. Modèle économique

- Freemium : X estimations/mois gratuites
- Abonnement mensuel (9-19€/mois estimé) : usage illimité + détection contrefaçon + dashboard

## 7. Roadmap synthétique

- **V1 (MVP)** : estimation prix/marge + détection contrefaçon (4 marques) + génération annonce + dashboard basique
- **V2** : plus de marques, scan photo direct sans formulaire, extension eBay/Leboncoin
- **V3** : appli mobile, publication auto Vinted, social proof entre revendeurs

Détail développement complet : voir `roadmap-dev.md`.

## 8. Risques principaux

- Fiabilité technique de la détection de contrefaçon → à tester AVANT de construire le reste (voir `PROMPTS.md` phase 0)
- Responsabilité légale si un verdict est faux → toujours formuler en "score de confiance", jamais en garantie (voir `coding-rules.md`)
- Accès aux données de vente Vinted (pas d'API officielle) → prévoir un plan B (estimation basée sur une base de données constituée manuellement au début)

## 9. Documents liés

- `vision.md` — vision long terme et positionnement
- `features.md` — spec détaillée de chaque fonctionnalité
- `database.md` — schéma de base de données
- `ui.md` — direction UI/UX
- `coding-rules.md` — conventions de code et règles à respecter
- `roadmap-dev.md` — plan de développement phase par phase
- `PROMPTS.md` — prompts Claude Code prêts à l'emploi, phase par phase
- `business-model.md` — pricing détaillé, coûts variables, métriques clés
- `competitive-analysis.md` — analyse détaillée des concurrents et différenciation
- `legal.md` — cadre juridique à faire valider (CGU, responsabilité, RGPD)
- `content-growth-strategy.md` — stratégie de contenu et boucle de croissance
