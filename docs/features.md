# Dénicho — Features

## 1. Estimation prix & marge

**Input**
- Marque, modèle/référence, taille, état (neuf/très bon/bon/satisfaisant)
- Prix d'achat (optionnel, pour calcul marge)
- Photo(s) optionnelle(s)

**Output**
- Fourchette de prix de revente basée sur des ventes comparables
- Marge estimée en € et en %
- Indicateur de vitesse de vente probable (rapide/moyen/lent) si donnée dispo

**Source de données**
- Ventes Vinted terminées (scraping, pas d'API officielle → prévoir un plan B manuel au démarrage)
- eBay sold listings (API officielle disponible)

## 2. Détection de contrefaçon (feature phare)

**Input**
- 3-4 photos ciblées : étiquette intérieure, logo, zip/boutons, matière de près

**Process**
1. Détection de la marque (auto ou renseignée par l'utilisateur)
2. Récupération de la checklist de points de contrôle propre à cette marque
3. Appel à un modèle vision avec prompt structuré comparant chaque point à l'image
4. Calcul d'un score de confiance global

**Output**
- Verdict : "authentique probable" / "suspect" / "contrefaçon probable"
- Détail par point de contrôle (ex : police du logo, position étiquette, qualité couture)
- Disclaimer visible : estimation IA, ne remplace pas une expertise professionnelle certifiée

**Scope V1 — toutes marques**
- Pas de restriction à 4 marques : l'utilisateur renseigne ou fait détecter n'importe quelle marque
- Approche technique : deux modes de fonctionnement
  1. **Marques avec checklist dédiée** (construite au fur et à mesure, en commençant par les plus contrefaites : Stone Island, Nike, Supreme, Ralph Lauren, Carhartt, TNF) → analyse précise point par point
  2. **Marques sans checklist encore construite** → analyse générique par le modèle vision (cohérence générale du logo, qualité de fabrication, étiquette) avec un niveau de confiance affiché plus prudent, et incitation à signaler le résultat pour enrichir la base
- La base `brand_reference_points` grandit avec le temps (priorité aux marques les plus demandées par les utilisateurs)

## 3. Génération d'annonce

**Input**
- Marque, modèle, taille, état, mesures, photos

**Output**
- Titre optimisé SEO Vinted
- Description structurée (état, mesures, defauts éventuels, mots-clés recherchés)
- Prix conseillé (relié à l'estimation de la feature 1)

## 4. Dashboard revendeur

- Stock en cours (liste des articles, statut : en stock / en vente / vendu)
- Marge totale et marge par article
- Historique des ventes
- Alerte : article en stock depuis X jours sans vente (seuil configurable)

## Priorisation de développement

Ordre recommandé (voir `roadmap-dev.md` pour détail) :
1. Détection de contrefaçon (valider la faisabilité technique en premier — c'est le risque principal)
2. Estimation prix/marge
3. Génération d'annonce
4. Dashboard
