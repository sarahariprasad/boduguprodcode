from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
# -----------------------
# Home Banner
# -----------------------
class HomeBannerView(models.Model):
    image = models.ImageField(upload_to='images/banner', default='images/default.png')
    title = models.CharField(max_length=100)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


# -----------------------
# Latest News
# -----------------------
class LatestNewsView(models.Model):
    image = models.ImageField(upload_to='images/latestnews', default='images/default.png')
    title = models.CharField(max_length=50)
    sticker = models.CharField(max_length=25)
    publisheddate = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=500)
    content = RichTextField(blank=True, null=True)
    extra_image1 = models.ImageField(upload_to='images/latestnews', blank=True, null=True)
    extra_image2 = models.ImageField(upload_to='images/latestnews', blank=True, null=True)
    extra_image3 = models.ImageField(upload_to='images/latestnews', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('latestnews_detail', args=[self.slug])

    def __str__(self):
        return self.title


# -----------------------
# Areas of Work
# -----------------------
class AreaOfWork(models.Model):
    banner_image = models.ImageField(upload_to="images/areas", default='images/default.png')
    title = models.CharField(max_length=150)
    description = RichTextField(blank=True, null=True)
    extra_image1 = models.ImageField(upload_to='images/areas', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("area_detail", args=[self.slug])

    def __str__(self):
        return self.title


# -----------------------
# Topic (belongs to Area of Work)
# -----------------------
class Topic(models.Model):
    banner_image = models.ImageField(upload_to="images/topics", default='images/default.png')
    title = models.CharField(max_length=150)
    short_description = models.CharField(max_length=300, blank=True, null=True)
    content = RichTextField(blank=True, null=True)
    area = models.ForeignKey(AreaOfWork, related_name="topics", on_delete=models.CASCADE)
    extra_image1 = models.ImageField(upload_to='images/topics', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("topic_detail", args=[self.area.slug, self.slug])

    def __str__(self):
        return f"{self.area.title} → {self.title}"
    


# -----------------------
# Donation Categories
# -----------------------
class DonationCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)

    class Meta:
        verbose_name_plural = "Donation Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class DonationAmount(models.Model):
    category = models.ForeignKey(DonationCategory, related_name="amounts", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.category.name} - ₹{self.amount}"


# -----------------------
# Campaigns (no category)
# -----------------------
class Campaign(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="campaigns/", blank=True, null=True)
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    raised_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_by = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def progress_percentage(self):
        if self.goal_amount > 0:
            return round((self.raised_amount / self.goal_amount) * 100, 2)
        return 0


class CampaignDonationAmount(models.Model):
    campaign = models.ForeignKey(Campaign, related_name="donation_amounts", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.campaign.title} - ₹{self.amount}"


# -----------------------
# Unified Donations
# -----------------------
class Donation(models.Model):
    campaign = models.ForeignKey(Campaign, blank=True, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(DonationCategory, blank=True, null=True, on_delete=models.SET_NULL)

    # Donor Info
    name = models.CharField(max_length=200)
    email = models.EmailField()
    dob = models.DateField(blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    certificate_80g = models.BooleanField(default=False)

    # Donation Info
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        base = f"{self.name} - ₹{self.amount}"
        if self.campaign and self.category:
            return f"{base} (Campaign: {self.campaign.title}, Category: {self.category.name})"
        elif self.campaign:
            return f"{base} (Campaign: {self.campaign.title})"
        elif self.category:
            return f"{base} (Category: {self.category.name})"
        return base


# -----------------------
# About Us
# -----------------------
class AboutUs(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField(blank=True, null=True)
    banner_image = models.ImageField(upload_to="about/", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "About Us"

    def __str__(self):
        return self.title


# -----------------------
# Stats
# -----------------------
class Stat(models.Model):
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="about/stats/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.title}: {self.value}"


# -----------------------
# Trustees
# -----------------------
class Trustee(models.Model):
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200, blank=True, null=True)
    bio = RichTextField(blank=True, null=True)
    photo = models.ImageField(upload_to="trustees/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


# -----------------------
# Media
# -----------------------
class MediaItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='uploads/images/', blank=True, null=True)
    video = models.FileField(upload_to='uploads/videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# -----------------------
# Impact Categories & Stories
# -----------------------
class ImpactCategory(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to="impact/category/", blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Impact Categories"

    def __str__(self):
        return self.name


class ImpactStory(models.Model):
    category = models.ForeignKey(ImpactCategory, related_name="stories", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="impact/stories/", blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# -----------------------
# Tenders
# -----------------------
class TenderNotice(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    document = models.FileField(upload_to="uploads/tenders/", blank=True, null=True)
    published_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
##Registerform#
class Village(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Mandal(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Domain(models.Model):
    title = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.title


class SubDomain(models.Model):
    title = models.CharField(max_length=200)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, null=True)
    is_open = models.BooleanField(default=True)  # Admin can toggle this
    max_slots = models.PositiveIntegerField(default=1)  # default 30

    def __str__(self):
        return self.title

    @property
    def current_applications(self):
        return self.registration_set.count()

    @property
    def is_full(self):
        return self.current_applications >= self.max_slots


    def __str__(self):
        return self.title


class Registration(models.Model):
    name = models.CharField(max_length=100)
    adhar_number = models.CharField(max_length=12, unique=True)
    adhar_upload = models.FileField(upload_to='adhar_uploads/')
    village = models.ForeignKey(Village, on_delete=models.CASCADE)
    mandal = models.ForeignKey(Mandal, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    subdomain = models.ForeignKey(SubDomain, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    qualification = models.CharField(max_length=200)
    comment = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.adhar_number})"

    def clean(self):
        if not self.domain.is_open:
            raise ValidationError(f"Applications for {self.domain.title} are currently closed.")

        if self.domain.is_full and not self.pk:  # prevent new applications if full
            raise ValidationError(
                f"Slots are completed for {self.domain.title}. "
                f"We will publish once slots are reopened."
            )

