from django.contrib import admin
from .models import (
    HomeBannerView, LatestNewsView, AreaOfWork, Topic,
    DonationCategory, DonationAmount,   # ✅ use DonationAmount
    Campaign, CampaignDonationAmount,
    Donation, AboutUs, MediaItem,
    ImpactCategory, ImpactStory,
    TenderNotice, Stat, Trustee,
    Registration, Village, Domain, Mandal, District, SubDomain
)


# -----------------------
# Home / News / Areas / Topics
# -----------------------
@admin.register(HomeBannerView)
class HomeBannerAdmin(admin.ModelAdmin):
    list_display = ("title", "image")


@admin.register(LatestNewsView)
class LatestNewsAdmin(admin.ModelAdmin):
    list_display = ("title", "sticker", "description")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(AreaOfWork)
class AreaOfWorkAdmin(admin.ModelAdmin):
    list_display = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("title", "area")
    prepopulated_fields = {"slug": ("title",)}


# -----------------------
# Donation Categories + Amounts
# -----------------------
class DonationAmountInline(admin.TabularInline):
    model = DonationAmount
    extra = 2


@admin.register(DonationCategory)
class DonationCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [DonationAmountInline]


# -----------------------
# Campaigns + Amounts
# -----------------------
class CampaignDonationAmountInline(admin.TabularInline):
    model = CampaignDonationAmount
    extra = 2


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("title", "goal_amount", "raised_amount", "progress_percentage")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CampaignDonationAmountInline]


# -----------------------
# Donations
# -----------------------
@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "amount","mobile", "certificate_80g", "created_at")
    list_filter = ("certificate_80g", "created_at")
    search_fields = ("name", "email", "mobile")


# -----------------------
# About Us / Stats / Trustees
# -----------------------
@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ("title", "updated_at")


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ("title", "value", "order")
    list_editable = ("order",)


@admin.register(Trustee)
class TrusteeAdmin(admin.ModelAdmin):
    list_display = ("name", "designation", "order")
    ordering = ("order", "name")


# -----------------------
# Media / Impact / Tenders
# -----------------------
@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")


@admin.register(ImpactCategory)
class ImpactCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "short_description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ImpactStory)
class ImpactStoryAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_at")


@admin.register(TenderNotice)
class TenderNoticeAdmin(admin.ModelAdmin):
    list_display = ("title", "published_date", "expiry_date", "is_active")
    list_filter = ("is_active", "published_date")
    search_fields = ("title", "description")

##registerform##
@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("name",)


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "adhar_number",
        "village",
        "domain",
        "mobile",
        "email",
        "created_at",
    )
    search_fields = ("name", "adhar_number", "mobile", "email")
    list_filter = ("village", "domain", "created_at")  # 🔹 filter sidebar


@admin.register(SubDomain)
class SubDomainAdmin(admin.ModelAdmin):
    list_display = ("title", "max_slots", "is_open", "total_registrations")
    list_editable = ("max_slots", "is_open")  # 🔹 inline edit
    search_fields = ("title",)
    list_filter = ("is_open",)

    def total_registrations(self, obj):
        return obj.registration_set.count()
    total_registrations.short_description = "Total Registrations"


@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Mandal)
class VillageAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(District)
class VillageAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
