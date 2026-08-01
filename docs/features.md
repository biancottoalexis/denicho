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

**Source de données (tranché)**

Approche en 2 étapes, pas de scraping Vinted tant que le point légal n'est pas validé (voir `legal.md`) :

1. **Lancement (V1 MVP)** : base manuelle. Alexis (et les beta testeurs) remplissent une table de référence de prix de revente observés par marque/modèle/état, à partir de son expérience BCT_Store. Volume minimum viable : au moins 15-20 références par marque prioritaire (Stone Island, Nike, Supreme, Ralph Lauren, Carhartt, TNF) avant le lancement beta. Format de saisie : simple formulaire admin ou fichier CSV importé.
2. **eBay sold listings (API officielle)** en complément dès que possible — légal, gratuit, mais couvre moins bien le marché Vinted-first visé.
3. **Scraping Vinted** : uniquement si validé légalement (voir `legal.md`, section scraping). Ne pas coder cette brique avant validation explicite. Si validé : anticiper le risque de ban IP (rotation de proxy, rate limiting).

Tant que (1) et (2) ne couvrent pas assez de références, l'estimation affiche une fourchette large avec un niveau de confiance explicite ("basé sur peu de données comparables").

**Contraintes techniques d'upload (tranchées)**

- **Formats acceptés** : JPG, PNG, HEIC (converti automatiquement en JPG côté backend à l'upload, car HEIC n'est pas lisible par tous les modèles vision — conversion via Pillow/pillow-heif)
- **Taille max par fichier** : 10 Mo
- **Résolution minimale** : 800x800 px — en dessous, l'upload est refusé côté frontend avec un message clair ("photo trop petite pour une analyse fiable, réessaie de plus près / meilleure lumière")
- **Détection de flou** : un contrôle basique de netteté (variance du Laplacien, calcul rapide côté backend à l'upload) rejette les photos manifestement floues avant même l'appel à l'API vision — évite de payer un appel API pour un résultat non fiable
- Ces contraintes s'appliquent aux deux features qui utilisent des photos (détection contrefaçon et estimation prix, si photo fournie)

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

**Méthodologie de scoring (tranchée, reproductible)**

- Chaque point de contrôle (logo, étiquette, couture, zip, matière) reçoit un score de confiance individuel de 0 à 100, retourné par le modèle vision
- Le score global est la **moyenne pondérée** des points disponibles, avec pondération par défaut égale entre tous les points analysés (pas de pondération différenciée en V1 — à affiner en V2 une fois des données réelles de feedback disponibles via `authenticity_feedback`)
- Seuils de verdict, appliqués au score global :
  - **≥ 75** → `authentique_probable`
  - **40 à 74** → `suspect`
  - **< 40** → `contrefacon_probable`
- Ces seuils sont une hypothèse de départ à valider/ajuster pendant la Phase 0 (voir critères de succès dans `roadmap-dev.md`) — ne pas les considérer figés avant le premier test réel

**Détection automatique de la marque (tranchée pour la V1)**

- **V1 : pas de détection auto par photo.** L'utilisateur saisit toujours la marque manuellement (champ texte libre relié à la table `brands`).
- Raison : la détection auto de marque par photo est un problème de vision distinct (classification, pas vérification d'authenticité) qui ajoute un risque technique supplémentaire non nécessaire pour valider l'angle produit. Ce n'est pas la priorité de la Phase 0.
- V2 (si le produit est validé) : ajouter un modèle de détection auto en amont, avec la saisie manuelle en fallback si la confiance de détection est faible.

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
