# Dénicho — PROMPTS (Claude Code, phase par phase)

Copie-colle ces prompts dans Claude Code, un par un, dans l'ordre. Chaque prompt suppose que **tous** les docs de `/docs` sont accessibles dans le repo, en particulier `decisions.md` (référentiel des choix tranchés — à lire en premier par Claude Code à chaque nouvelle session).

---

## Phase 0 — Test de faisabilité détection contrefaçon

**`test-authenticity.py` existe déjà** à la racine du repo (marque en argument + 2 à 4 images, checklists dédiées pour 50 marques, sortie JSON structurée avec score par point + score global + verdict selon les seuils de `decisions.md`). Ne pas le recréer depuis zéro. Ce qui manque encore et reste à faire :

```
Lis /docs/decisions.md, /docs/PRD-MASTER.md, /docs/features.md section 2 (détection de contrefaçon) et /docs/roadmap-dev.md section "Critères de succès chiffrés".
Le script test-authenticity.py existe déjà (marque + 2-4 images, 50 checklists dédiées, verdict/score selon les seuils de decisions.md) — adapte-le si besoin mais ne le recrée pas.
Crée un script batch (run-test-set.py) qui prend un dossier contenant plusieurs articles (chacun avec ses 2-4 photos) et leur verdict réel connu (nommage type "stone-island-vrai-01/"), appelle test-authenticity.py sur chacun, et calcule le taux de bonnes réponses sur l'ensemble.
Objectif : constituer un jeu de test d'au moins 20 articles connus (authentiques/contrefaits, au moins 2 marques) et mesurer si on atteint le seuil de 85% de verdicts corrects. Pas construire de produit, juste valider la fiabilité — c'est cette mesure réelle qui manque encore avant de passer à la Phase 1.
```

## Phase 1 — Setup projet

```
Lis /docs/decisions.md puis tous les autres fichiers dans /docs.
Initialise un projet avec : frontend React + Tailwind + shadcn/ui, backend FastAPI (Python), PostgreSQL.
Respecte la structure de dossiers et les conventions définies dans /docs/coding-rules.md.
Crée les tables de la base de données décrites dans /docs/database.md via une migration (Alembic).
Mets en place une auth basique utilisateur (email + mot de passe hashé, JWT + refresh token).
Crée un fichier .env.example listant toutes les variables attendues, et vérifie que .env est bien dans .gitignore.
```

## Phase 2 — Détection de contrefaçon (MVP)

```
Lis /docs/features.md section 2 et /docs/ui.md.
Construis la feature de détection de contrefaçon, ouverte à toutes les marques :
- formulaire d'upload de 3-4 photos guidées (étiquette, logo, zip, matière) + champ marque (texte libre)
- endpoint backend qui vérifie si la marque a une checklist dédiée dans brand_reference_points, sinon utilise le prompt générique (basé sur le test de phase 0)
- stockage du résultat dans la table authenticity_checks
- affichage frontend du verdict avec badge coloré + détail par point + mention du mode (précis/générique) + disclaimer visible (voir coding-rules.md, le disclaimer doit être renvoyé par le backend)
Pré-remplis la checklist dédiée pour Stone Island uniquement pour ce MVP, le reste des marques passe en mode générique.
```

## Phase 3 — Estimation prix/marge

```
Lis /docs/features.md section 1 et /docs/database.md.
Construis la feature d'estimation prix/marge :
- formulaire article (marque, modèle, taille, état, prix d'achat optionnel)
- logique de calcul de fourchette de prix (si pas encore de source de données réelle, utilise une table brand_reference_points ou une base manuelle temporaire à structurer)
- affichage du résultat avec marge estimée en € et %
```

## Phase 4 — Génération d'annonce

```
Lis /docs/features.md section 3.
Construis la génération d'annonce Vinted :
- à partir des données de l'article (marque, modèle, taille, état, mesures)
- génère titre optimisé SEO, description structurée, prix conseillé (relié à l'estimation de la phase 3)
- affiche un preview avec bouton copier
```

## Phase 5 — Dashboard

```
Lis /docs/features.md section 4 et /docs/ui.md.
Construis le dashboard revendeur : liste des articles avec statut, marge totale et par article, alerte pour les articles en stock depuis plus de X jours (seuil configurable).
```

## Notes générales pour toutes les phases

- Toujours relire le fichier `coding-rules.md` avant de générer du code pour respecter les conventions
- Ne jamais formuler un verdict d'authenticité comme une certitude — toujours "probable" / "score de confiance"
- Committer après chaque phase avec un message clair
