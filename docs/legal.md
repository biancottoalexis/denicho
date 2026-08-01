# Dénicho — Cadre légal (à faire valider par un professionnel)

Important : ceci est une base de travail, pas un avis juridique. Vu que la feature phare touche à l'authenticité de produits de marque, il est fortement recommandé de faire relire les CGU/CGV par un avocat ou un service comme Legalstart avant le lancement public.

## Point le plus urgent — statut du scraping Vinted

C'est actuellement le vrai risque juridique du projet, plus urgent que le verdict de contrefaçon lui-même. Vinted n'a pas d'API publique officielle pour les ventes terminées ; scraper ses pages pose potentiellement une question de respect des conditions d'utilisation de la plateforme et, selon la méthode, de la réglementation sur l'accès à des systèmes de traitement de données.

**Ceci n'est pas un avis juridique** — la légalité exacte dépend de la méthode technique utilisée (fréquence, volume, contournement ou non de protections) et évolue selon la jurisprudence. Avant de coder la moindre brique de scraping Vinted (voir `features.md` Feature 1) :
1. Ne pas commencer le scraping avant validation
2. Poser la question explicitement à l'avocat consulté (voir budget ci-dessous), avec description précise de la méthode envisagée
3. En attendant, la Feature 1 tourne uniquement sur la base manuelle + eBay (voir `features.md`) — cette limitation est volontaire, pas un oubli

## Points à couvrir dans les CGU

1. **Nature du service** : Dénicho fournit une estimation indicative basée sur un modèle d'IA, pas une expertise d'authentification certifiée. Aucune garantie n'est donnée sur l'exactitude du verdict.
2. **Limitation de responsabilité** : l'utilisateur reste seul responsable de sa décision d'achat/vente ; Dénicho ne peut être tenu responsable d'une perte financière liée à une estimation erronée.
3. **Propriété intellectuelle des marques mentionnées** : Dénicho ne prétend pas être affilié aux marques (Stone Island, Nike, Supreme, Ralph Lauren) — mention explicite de non-affiliation à inclure.
4. **Données utilisateur** : photos uploadées, conservation 90 jours puis purge automatique (voir `database.md` — politique de rétention), consentement RGPD explicite tracé via `users.consent_given_at` avant tout upload.

## Statut juridique de la micro-entreprise

Comme Nexora/ZeroToFirst, Dénicho peut démarrer sous la même micro-entreprise une fois ouverte, en tant qu'activité secondaire, tant que le chiffre d'affaires reste sous le seuil micro. À réévaluer si le SaaS décolle (passage en société).

## Budget et délai pour la relecture avocat

- Budget indicatif pour une relecture CGU/CGV + question scraping par un avocat spécialisé numérique, ou service type Legalstart : compter environ 300-800€ pour un package CGU/CGV standard (le tarif exact dépend du prestataire choisi, à confirmer par devis) — un service en ligne type Legalstart est généralement moins cher qu'un cabinet d'avocat classique mais donne un cadre moins personnalisé
- Délai à prévoir : 1-2 semaines pour un premier retour
- Ce point doit être traité **avant** la phase de lancement beta publique (Phase 6 de `roadmap-dev.md`), pas avant le développement technique — la Phase 0 et le prototype peuvent avancer en parallèle

## Risque spécifique identifié

Le sujet "détection de contrefaçon" est sensible : si Dénicho affirme à tort qu'un article authentique est un faux (ou l'inverse), ça peut avoir un impact commercial pour l'utilisateur. D'où l'importance du point 1 et 2 ci-dessus, à formaliser clairement avant tout lancement public, même en beta.
