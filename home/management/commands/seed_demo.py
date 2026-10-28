from datetime import date

from django.core.management.base import BaseCommand
from wagtail.models import Page, Site

from home.models import GalleryImage, HomePage, Product, SocialPost, StoreSettings


PRODUCTS = [
    {
        "slug": "viandes-fraiches",
        "name": "Viandes fraîches",
        "category": Product.Category.BOUCHERIE,
        "tag": "LE COMPTOIR",
        "description": "Bœuf, viande hachée et coupes du jour. Demandez les disponibilités.",
        "fallback_image": "viande.jpg",
        "sort_order": 1,
    },
    {
        "slug": "poulet-frais",
        "name": "Poulet frais",
        "category": Product.Category.VOLAILLE,
        "tag": "FRAÎCHE DU JOUR",
        "description": "Découvrez les coupes disponibles au comptoir.",
        "fallback_image": "instagram-specials.jpg",
        "sort_order": 2,
    },
    {
        "slug": "agneau-du-quebec",
        "name": "Agneau du Québec",
        "category": Product.Category.AGNEAU,
        "tag": "CHOIX DU BOUCHER",
        "description": "Une viande savoureuse, sélectionnée avec soin.",
        "fallback_image": "comptoir.jpg",
        "sort_order": 3,
    },
    {
        "slug": "merguez-grillades",
        "name": "Merguez & grillades",
        "category": Product.Category.GRILLADES,
        "tag": "À GRILLER",
        "description": "Le goût du charbon et les saveurs du barbecue.",
        "fallback_image": "instagram-epicerie.jpg",
        "sort_order": 4,
    },
    {
        "slug": "epicerie-mediterraneenne",
        "name": "Les saveurs méditerranéennes",
        "category": Product.Category.EPICERIE,
        "tag": "ÉPICERIE MÉDITERRANÉENNE",
        "description": "Épices, olives, conserves, fromages et produits du Maghreb.",
        "fallback_image": "instagram-promotions.jpg",
        "sort_order": 5,
    },
    {
        "slug": "fruits-legumes",
        "name": "Fraîcheur du marché",
        "category": Product.Category.FRAIS,
        "tag": "PRODUITS FRAIS",
        "description": "Fruits et légumes du jour, selon les arrivages.",
        "fallback_image": "boutique.jpg",
        "sort_order": 6,
    },
]

POSTS = [
    {
        "title": "Le goût du charbon",
        "post_type": SocialPost.Kind.REEL,
        "caption": "Les grillades de Melia",
        "post_url": "https://www.instagram.com/boucheriegrillademelia/reel/DbpE9KXuQPP/",
        "published_at": date(2026, 8, 4),
        "fallback_image": "instagram-grillade.jpg",
        "sort_order": 1,
    },
    {
        "title": "Viandes et produits frais",
        "post_type": SocialPost.Kind.PUBLICATION,
        "caption": "Des offres de la semaine en boutique",
        "post_url": "https://www.instagram.com/boucheriegrillademelia/p/DSJaRc6Dfil/",
        "published_at": date(2025, 12, 11),
        "fallback_image": "instagram-specials.jpg",
        "sort_order": 2,
    },
    {
        "title": "Épicerie Melia",
        "post_type": SocialPost.Kind.PUBLICATION,
        "caption": "Épicerie fine, produits marocains, épices et olives",
        "post_url": "https://www.instagram.com/boucheriegrillademelia/p/DJEiHl5uEDu/",
        "fallback_image": "instagram-promotions.jpg",
        "sort_order": 3,
    },
    {
        "title": "Promotions Melia",
        "post_type": SocialPost.Kind.PUBLICATION,
        "caption": "Une sélection de viandes et de produits frais",
        "post_url": "https://www.instagram.com/boucheriegrillademelia/p/DPFS2kjkpNu/",
        "published_at": date(2025, 9, 26),
        "fallback_image": "instagram-promotions.jpg",
        "sort_order": 4,
    },
]

MAP_GALLERY = [
    {"title": f"La boutique Melia · {i:02d}", "category": category, "caption": caption,
     "fallback_image": f"maps-{i:02d}.jpg", "source_url": "https://www.google.com/maps/place/Boucherie+Melia+Halal/"}
    for i, (category, caption) in enumerate([
        ("boucherie", "Le comptoir et les viandes du jour"), ("boutique", "Un aperçu de la boutique"),
        ("epicerie", "Les produits de l’épicerie"), ("grillades", "Les saveurs à partager"),
        ("boutique", "La boutique à Saint-Jérôme"), ("boucherie", "Au comptoir"),
        ("epicerie", "Les essentiels du marché"), ("boucherie", "Les produits de la maison"),
        ("boutique", "Un regard sur la boutique"), ("epicerie", "L’épicerie Melia"),
        ("grillades", "Préparations et grillades"), ("boutique", "Bienvenue chez Melia"),
        ("epicerie", "Les saveurs méditerranéennes"), ("boucherie", "Sélection du comptoir"),
        ("boutique", "La boutique Melia"), ("epicerie", "Produits et épicerie"),
        ("boucherie", "Des viandes choisies avec soin"), ("boutique", "À découvrir en boutique"),
        ("grillades", "Les idées repas de Melia"), ("epicerie", "Les produits du quotidien"),
        ("boucherie", "Le savoir-faire du comptoir"), ("grillades", "De quoi régaler tout le monde"),
        ("boucherie", "Les viandes du comptoir"), ("boutique", "À deux pas de chez vous"),
        ("epicerie", "La sélection de l’épicerie"),
    ], start=1)
]
MAP_GALLERY += [
    {"title": title, "category": "boutique", "caption": caption,
     "fallback_image": f"maps-streetview-{i:02d}.jpg", "source_url": "https://www.google.com/maps/place/Boucherie+Melia+Halal/"}
    for i, (title, caption) in enumerate([
        ("La façade de la boutique", "Située au 297, rue Labelle"),
        ("Autour de la boutique", "Un aperçu de Saint-Jérôme"),
        ("Entrée de la boutique", "Repérez facilement la boutique"),
    ], start=1)
]

INSTAGRAM_GALLERY = [
    ("DSJaRc6Dfil", "Offres et produits frais", "Des nouvelles de la sélection en boutique", "epicerie"),
    ("DPFS2kjkpNu", "Les offres de la semaine", "Viandes et produits frais", "boucherie"),
    ("DJEiHl5uEDu", "Épicerie Melia", "Épicerie, charcuteries, fromages et épices", "epicerie"),
    ("DCKH-GsP_JM", "En coulisses", "Un moment chez Melia", "publications"),
    ("DN9czURiP52", "Le quotidien de la boutique", "Viandes, volaille et comptoir", "boucherie"),
    ("DKGzR6MiuqP", "Saveurs méditerranéennes", "Épicerie, épices et produits du Maghreb", "epicerie"),
    ("DRqJeZuE-aR", "Les nouvelles de Melia", "Un aperçu de la boutique", "publications"),
    ("DbpE9KXuQPP", "Le goût du charbon", "Grillades et saveurs à partager", "grillades"),
    ("DGpem5COMgH", "Sélection du Ramadan", "Dates, pains, épices et produits de saison", "epicerie"),
]


class Command(BaseCommand):
    help = "Crée le contenu de démonstration Melia (sans écraser les contenus existants)."

    def handle(self, *args, **options):
        root = Page.get_first_root_node()
        homepage = HomePage.objects.filter(depth=2).first()
        if homepage is None:
            homepage = root.add_child(
                instance=HomePage(title="Boucherie Épicerie Grillade Melia Halal", slug="home")
            )
        if not homepage.live or homepage.title == "Home":
            homepage.title = "Boucherie Épicerie Grillade Melia Halal"
            homepage.hero_line_one = "Le goût"
            homepage.hero_line_two = "du"
            homepage.hero_highlight = "vrai."
            homepage.hero_intro = (
                "Des viandes choisies avec soin, des grillades savoureuses et les essentiels de l’épicerie — "
                "servis avec le sourire, au cœur de Saint-Jérôme."
            )
            homepage.intro_heading = "Les bons repas commencent"
            homepage.intro_accent = "ici."
            homepage.intro_lead = (
                "Une bonne boucherie, c’est plus qu’un comptoir. C’est le bon conseil, la coupe préparée comme il faut et le plaisir de revenir."
            )
            homepage.intro_body = (
                "Chez Melia, on prend le temps de bien vous servir. Pour le repas de tous les jours comme pour les grandes tablées, "
                "découvrez des produits soigneusement choisis et un accueil chaleureux au cœur de Saint-Jérôme."
            )
            homepage.story_heading = "Vos repas."
            homepage.story_pre_accent = "Notre"
            homepage.story_accent = "passion."
            homepage.story_body = (
                "On aime savoir que nos produits se retrouvent au centre de vos repas et de vos plus beaux moments. "
                "Passez nous voir — on s’occupe du reste."
            )
            homepage.save()
            homepage.save_revision().publish()

        site, _ = Site.objects.get_or_create(
            is_default_site=True,
            defaults={"hostname": "localhost", "port": 8000, "root_page": homepage, "site_name": "Melia"},
        )
        site.root_page = homepage
        site.site_name = "Boucherie Melia"
        site.save()

        StoreSettings.objects.get_or_create(
            site=site,
            defaults={
                "business_name": "Boucherie Épicerie Grillade Melia Halal",
                "phone": "(450) 436-3783",
                "street_address": "297, rue Labelle",
                "city_postal": "Saint-Jérôme, QC J7Z 5L2",
                "opening_note": "Appelez-nous pour connaître les heures du jour.",
                "google_rating": "4.9",
                "google_review_count": 95,
                "featured_review": "Le service est top, le personnel est souriant et très serviable.",
                "google_reviews_url": "https://www.google.com/maps/search/?api=1&query=Boucherie+Melia+Halal+297+Rue+Labelle+Saint-J%C3%A9r%C3%B4me",
            },
        )

        for data in PRODUCTS:
            Product.objects.get_or_create(slug=data["slug"], defaults=data)
        for data in POSTS:
            SocialPost.objects.get_or_create(post_url=data["post_url"], defaults=data)

        for order, data in enumerate(MAP_GALLERY, start=1):
            data = {**data, "sort_order": order}
            GalleryImage.objects.get_or_create(fallback_image=data["fallback_image"], defaults=data)
        for order, (post_id, title, caption, category) in enumerate(INSTAGRAM_GALLERY, start=1):
            fallback = f"instagram-{post_id}.jpg"
            source = f"https://www.instagram.com/boucheriegrillademelia/{'reel' if post_id in {'DCKH-GsP_JM','DN9czURiP52','DKGzR6MiuqP','DRqJeZuE-aR','DbpE9KXuQPP'} else 'p'}/{post_id}/"
            if post_id == "DJEiHl5uEDu":
                source = f"https://www.instagram.com/boucheriegrillademelia/p/{post_id}/"
            GalleryImage.objects.get_or_create(
                source_url=source,
                defaults={"title": title, "caption": caption, "category": category,
                          "fallback_image": fallback, "sort_order": len(MAP_GALLERY) + order},
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Contenu de démonstration prêt : {Product.objects.count()} produits, "
                f"{SocialPost.objects.count()} publications, {GalleryImage.objects.count()} photos de galerie, "
                "page d’accueil et paramètres boutique."
            )
        )
