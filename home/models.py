from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.images.models import Image
from wagtail.models import Page
from wagtail.search import index
from wagtail.snippets.models import register_snippet


class HomePage(Page):
    """Editable landing page for the shop."""

    hero_line_one = models.CharField(max_length=90, default="Le goût")
    hero_line_two = models.CharField(max_length=90, default="du")
    hero_highlight = models.CharField(max_length=90, default="vrai.")
    hero_image = models.ForeignKey(
        Image, null=True, blank=True, on_delete=models.SET_NULL, related_name="+", verbose_name="Photo de bannière"
    )
    hero_intro = models.TextField(
        default=(
            "Des viandes choisies avec soin, des grillades savoureuses et les "
            "essentiels de l’épicerie — servis avec le sourire, au cœur de Saint-Jérôme."
        )
    )
    intro_heading = models.CharField(max_length=120, default="Les bons repas commencent ici.")
    intro_lead = models.TextField(
        default="Une bonne boucherie, c’est plus qu’un comptoir. C’est le bon conseil, la coupe préparée comme il faut et le plaisir de revenir."
    )
    intro_body = models.TextField(
        default="Chez Melia, on prend le temps de bien vous servir. Pour le repas de tous les jours comme pour les grandes tablées, découvrez des produits soigneusement choisis et un accueil chaleureux au cœur de Saint-Jérôme."
    )
    intro_accent = models.CharField(max_length=80, default="ici.")
    story_heading = models.CharField(max_length=120, default="Vos repas.")
    story_pre_accent = models.CharField(max_length=50, default="Notre")
    story_accent = models.CharField(max_length=80, default="passion.")
    story_image = models.ForeignKey(
        Image, null=True, blank=True, on_delete=models.SET_NULL, related_name="+", verbose_name="Photo de la boutique"
    )
    story_body = models.TextField(
        default="On aime savoir que nos produits se retrouvent au centre de vos repas et de vos plus beaux moments. Passez nous voir — on s’occupe du reste."
    )
    featured_review = models.TextField(
        default="Le service est top, le personnel est souriant et très serviable."
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [FieldPanel("hero_line_one"), FieldPanel("hero_line_two"), FieldPanel("hero_highlight"), FieldPanel("hero_intro"), FieldPanel("hero_image")],
            heading="Bannière d’accueil",
        ),
        MultiFieldPanel(
            [FieldPanel("intro_heading"), FieldPanel("intro_accent"), FieldPanel("intro_lead"), FieldPanel("intro_body")],
            heading="Notre maison",
        ),
        MultiFieldPanel(
            [FieldPanel("story_heading"), FieldPanel("story_pre_accent"), FieldPanel("story_accent"), FieldPanel("story_body"), FieldPanel("story_image")],
            heading="Notre histoire",
        ),
        MultiFieldPanel([FieldPanel("featured_review")], heading="Avis mis en avant"),
    ]

    parent_page_types = ["wagtailcore.Page"]
    subpage_types = []
    max_count = 1

    search_fields = Page.search_fields + [
        index.SearchField("hero_intro"),
        index.SearchField("intro_body"),
    ]

    def get_context(self, request, *args, **kwargs):
        from django.db.models import Count

        context = super().get_context(request, *args, **kwargs)
        products = Product.objects.filter(is_active=True).select_related("image").order_by("sort_order", "name")
        counts = {
            item["category"]: item["total"]
            for item in products.values("category").annotate(total=Count("id"))
        }
        context["products"] = products
        context["product_categories"] = [
            {"slug": slug, "label": label, "count": counts.get(slug, 0)}
            for slug, label in Product.Category.choices
            if counts.get(slug, 0)
        ]
        context["social_posts"] = SocialPost.objects.filter(is_active=True).select_related("image")
        gallery_images = GalleryImage.objects.filter(is_active=True).select_related("image")
        context["gallery_images"] = gallery_images
        context["gallery_categories"] = [
            {"slug": slug, "label": label}
            for slug, label in GalleryImage.Category.choices
            if gallery_images.filter(category=slug).exists()
        ]
        context["store"] = StoreSettings.for_request(request)
        return context


@register_snippet
class Product(models.Model):
    class Category(models.TextChoices):
        BOUCHERIE = "boucherie", "Boucherie"
        VOLAILLE = "volaille", "Volaille"
        AGNEAU = "agneau", "Agneau"
        GRILLADES = "grillades", "Grillades"
        EPICERIE = "epicerie", "Épicerie méditerranéenne"
        FRAIS = "frais", "Fruits et légumes"

    name = models.CharField("Nom du produit", max_length=100)
    slug = models.SlugField(unique=True)
    category = models.CharField("Catégorie", max_length=20, choices=Category.choices)
    tag = models.CharField("Étiquette", max_length=60, blank=True)
    description = models.CharField("Description", max_length=220)
    image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Photo du produit",
    )
    fallback_image = models.CharField(
        "Photo de démonstration", max_length=120, blank=True, help_text="Image initiale utilisée si aucune photo n’est téléversée."
    )
    sort_order = models.PositiveSmallIntegerField("Ordre d’affichage", default=0)
    is_active = models.BooleanField("Afficher sur le site", default=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("category"),
        FieldPanel("tag"),
        FieldPanel("description"),
        FieldPanel("image"),
        FieldPanel("fallback_image"),
        FieldPanel("sort_order"),
        FieldPanel("is_active"),
    ]

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name = "produit"
        verbose_name_plural = "produits"

    def __str__(self):
        return self.name


@register_snippet
class SocialPost(models.Model):
    class Kind(models.TextChoices):
        PUBLICATION = "publication", "Publication"
        REEL = "reel", "Reel vidéo"

    title = models.CharField("Titre", max_length=100)
    post_type = models.CharField("Format", max_length=14, choices=Kind.choices, default=Kind.PUBLICATION)
    caption = models.CharField("Texte court", max_length=180, blank=True)
    post_url = models.URLField("Lien Instagram")
    published_at = models.DateField("Date de publication", null=True, blank=True)
    image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Visuel",
    )
    fallback_image = models.CharField("Visuel de démonstration", max_length=120, blank=True)
    sort_order = models.PositiveSmallIntegerField("Ordre d’affichage", default=0)
    is_active = models.BooleanField("Afficher sur le site", default=True)

    panels = [
        FieldPanel("title"),
        FieldPanel("post_type"),
        FieldPanel("caption"),
        FieldPanel("post_url"),
        FieldPanel("published_at"),
        FieldPanel("image"),
        FieldPanel("fallback_image"),
        FieldPanel("sort_order"),
        FieldPanel("is_active"),
    ]

    class Meta:
        ordering = ["sort_order", "-published_at"]
        verbose_name = "publication sociale"
        verbose_name_plural = "publications sociales"

    def __str__(self):
        return self.title


@register_snippet
class GalleryImage(models.Model):
    class Category(models.TextChoices):
        BOUCHERIE = "boucherie", "Boucherie"
        BOUTIQUE = "boutique", "La boutique"
        EPICERIE = "epicerie", "Épicerie"
        GRILLADES = "grillades", "Grillades"
        PUBLICATIONS = "publications", "Publications"

    title = models.CharField("Titre", max_length=100)
    category = models.CharField("Catégorie", max_length=20, choices=Category.choices, default=Category.BOUTIQUE)
    caption = models.CharField("Description", max_length=180, blank=True)
    source_url = models.URLField("Lien de la photo", blank=True)
    image = models.ForeignKey(
        Image, null=True, blank=True, on_delete=models.SET_NULL, related_name="+", verbose_name="Photo téléversée"
    )
    fallback_image = models.CharField(
        "Photo fournie", max_length=120, blank=True, help_text="Photo initiale ; une photo téléversée la remplacera."
    )
    sort_order = models.PositiveSmallIntegerField("Ordre d’affichage", default=0)
    is_active = models.BooleanField("Afficher sur le site", default=True)

    panels = [
        FieldPanel("title"), FieldPanel("category"), FieldPanel("caption"), FieldPanel("source_url"),
        FieldPanel("image"), FieldPanel("fallback_image"), FieldPanel("sort_order"), FieldPanel("is_active"),
    ]

    class Meta:
        ordering = ["sort_order", "title"]
        verbose_name = "photo de la galerie"
        verbose_name_plural = "galerie photos"

    def __str__(self):
        return self.title


@register_setting(icon="site")
class StoreSettings(BaseSiteSetting):
    business_name = models.CharField("Nom commercial", max_length=120, default="Boucherie Épicerie Grillade Melia Halal")
    phone = models.CharField("Téléphone", max_length=30, default="(450) 436-3783")
    street_address = models.CharField("Adresse", max_length=150, default="297, rue Labelle")
    city_postal = models.CharField("Ville et code postal", max_length=120, default="Saint-Jérôme, QC J7Z 5L2")
    opening_note = models.CharField("Horaires à afficher", max_length=160, default="Appelez-nous pour connaître les heures du jour.")
    map_url = models.URLField(
        "Lien Google Maps",
        default="https://www.google.com/maps/dir/?api=1&destination=Boucherie+Melia+Halal%2C+297+Rue+Labelle%2C+Saint-J%C3%A9r%C3%B4me%2C+QC",
    )
    instagram_url = models.URLField("Instagram", default="https://www.instagram.com/boucheriegrillademelia/")
    facebook_url = models.URLField("Facebook", default="https://www.facebook.com/profile.php?id=61564189628864")
    google_rating = models.DecimalField("Note Google", max_digits=2, decimal_places=1, default=4.9)
    google_review_count = models.PositiveSmallIntegerField("Nombre d’avis Google", default=95)
    featured_review = models.TextField(
        "Avis mis en avant",
        default="Le service est top, le personnel est souriant et très serviable.",
    )
    google_reviews_url = models.URLField(
        "Lien vers les avis Google",
        default="https://www.google.com/maps/search/?api=1&query=Boucherie+Melia+Halal+297+Rue+Labelle+Saint-J%C3%A9r%C3%B4me",
    )

    panels = [
        FieldPanel("business_name"),
        FieldPanel("phone"),
        FieldPanel("street_address"),
        FieldPanel("city_postal"),
        FieldPanel("opening_note"),
        FieldPanel("map_url"),
        MultiFieldPanel([FieldPanel("instagram_url"), FieldPanel("facebook_url")], heading="Réseaux sociaux"),
        MultiFieldPanel(
            [FieldPanel("google_rating"), FieldPanel("google_review_count"), FieldPanel("featured_review"), FieldPanel("google_reviews_url")],
            heading="Avis Google",
        ),
    ]

    class Meta:
        verbose_name = "Informations de la boutique"
