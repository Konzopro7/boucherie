# Démo — Boucherie Épicerie Grillade Melia Halal

Site vitrine responsive en français, réalisé avec Django et Wagtail à partir des informations publiques et des photos fournies pour la boutique. La démo comprend une galerie filtrable et une interface d’administration pour gérer les produits, les photos, les publications et les coordonnées.

## Lancer le site sous Windows

Depuis le dossier du projet (`Boucheriemelia`) :

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_demo
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

Ouvrir ensuite le site sur <http://127.0.0.1:8000/> et l’administration sur <http://127.0.0.1:8000/admin/>. Dans Wagtail, les photos sont gérées sous **Snippets → Galerie photos**.

La page statique `index.html` est aussi disponible pour un aperçu rapide, sans serveur Django.

## Contenu de démonstration

- Galerie photo avec filtres par boucherie, boutique, épicerie, grillades et publications
- Photos locales inspirées des références Google Maps et Instagram fournies
- Filtres produits, navigation mobile et formulaire de demande par téléphone
- Liens vers Instagram, Facebook, Google Maps et téléphone
- Respect du réglage système de réduction des animations

Les produits, avis et offres illustrent le contenu fourni et ne sont pas garantis comme étant encore en vigueur. Les disponibilités et horaires sont à confirmer auprès du commerce. Le site ne traite pas de paiement.