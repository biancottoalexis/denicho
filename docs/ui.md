# Dénicho — UI

## Direction générale

Cohérent avec la patte visuelle ZeroToFirst : dark mode, accent violet (#8B5CF6 ou variante), police Inter.
Adapté ici avec un accent qui évoque le "flair"/la trouvaille (option : garder le violet pour cohérence de marque perso, ou tester un accent orange/ambre qui évoque la friperie/vintage).

## Écrans principaux

1. **Dashboard** — vue d'ensemble stock, marge totale, alertes
2. **Ajout article** — formulaire marque/modèle/taille/état + upload photos
3. **Résultat estimation** — fourchette prix + marge, avec breakdown des ventes comparables utilisées
4. **Résultat détection contrefaçon** — score visuel (jauge ou badge coloré), détail par point de contrôle, disclaimer visible en permanence
5. **Annonce générée** — preview de l'annonce Vinted (titre/description/prix), bouton copier

## Principes UX

- Le disclaimer sur la détection de contrefaçon doit être visible sans être anxiogène — ton informatif, pas alarmiste
- Upload photo guidé (ex : mini-illustrations montrant où prendre chaque photo : étiquette, logo, zip, matière) pour maximiser la qualité de la détection
- Dashboard doit répondre en un coup d'oeil à "qu'est-ce qui dort en stock depuis trop longtemps"

## Composants réutilisables

- Badge de verdict (vert/orange/rouge) pour authenticité
- Carte article (photo + marque + statut + marge)
- Jauge de score de confiance

## Mobile-first (angle mort corrigé)

L'usage réel de l'app se fait très majoritairement au téléphone : un revendeur photographie un article directement en friperie ou vide-grenier. Toute l'interface doit être conçue mobile-first, pas adaptée après coup :
- Formulaire d'upload photo pensé pour la caméra du téléphone (accès direct à l'appareil photo, pas juste un input file générique)
- Résultats (estimation, détection contrefaçon) lisibles en une seule colonne sur petit écran, sans scroll horizontal
- Le dashboard peut avoir une version desktop plus riche (tableaux, export CSV), mais l'ajout d'article et la détection contrefaçon doivent être irréprochables sur mobile en priorité

## Librairie de composants (tranchée)

**shadcn/ui** (avec Tailwind, cohérent avec la stack) — pour que Claude Code réutilise des composants existants (boutons, cartes, badges, formulaires) au lieu de réinventer un design system à chaque session. Toute nouvelle session Claude Code doit vérifier les composants shadcn/ui déjà utilisés avant d'en créer de nouveaux.
