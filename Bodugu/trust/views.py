from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    HomeBannerView, LatestNewsView, AreaOfWork, Topic,
    DonationCategory, DonationAmount,
    Campaign, CampaignDonationAmount,
    Donation, AboutUs, MediaItem, ImpactCategory, TenderNotice, Stat, Trustee,
    Campaign, DonationCategory, Donation,
    Registration, Village, Domain, Mandal, District, SubDomain
)

# -----------------------
# Home page
# -----------------------
def home(request):
    homebanner = HomeBannerView.objects.all()
    latestnews = LatestNewsView.objects.all()
    areas = AreaOfWork.objects.all()
    return render(request, 'trust/home.html', {
        'homebanner': homebanner,
        'latestnews': latestnews,
        'areas': areas,
    })


# -----------------------
# News / Areas / Topics
# -----------------------
def latestnews_detail(request, slug):
    news = get_object_or_404(LatestNewsView, slug=slug)
    return render(request, 'trust/latestnews_detail.html', {'news': news})


def area_detail(request, slug):
    area = get_object_or_404(AreaOfWork, slug=slug)
    return render(request, "trust/area_detail.html", {"area": area})


def topic_detail(request, area_slug, topic_slug):
    topic = get_object_or_404(Topic, area__slug=area_slug, slug=topic_slug)
    return render(request, "trust/topic_detail.html", {"topic": topic})


# -----------------------
# How to Help (Donation Categories)
# -----------------------
def how_to_help(request, category=None):
    categories = DonationCategory.objects.all()
    selected_category = None
    amounts = None

    if categories.exists():
        if category:
            selected_category = get_object_or_404(DonationCategory, slug=category)
        else:
            selected_category = categories.first()
        if selected_category:
            amounts = selected_category.amounts.all()

    return render(request, "trust/how_to_help.html", {
        "categories": categories,
        "selected_category": selected_category,
        "amounts": amounts,
    })


# -----------------------
# Campaigns
# -----------------------
def campaign_list(request):
    campaigns = Campaign.objects.all().order_by("-id")
    return render(request, "trust/campaign_list.html", {"campaigns": campaigns})


def campaign_detail(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    donation_options = campaign.donation_amounts.all()  # Related name in CampaignDonationAmount
    return render(request, "trust/campaign_detail.html", {
        "campaign": campaign,
        "donation_options": donation_options,
    })


# -----------------------
# Unified Donation Form
# -----------------------
def donation_form(request, slug=None, category_slug=None):
    campaign = None
    category = None
    donation_options = []

    if slug:
        campaign = get_object_or_404(Campaign, slug=slug)
        donation_options = campaign.donation_amounts.all()
    elif category_slug:
        category = get_object_or_404(DonationCategory, slug=category_slug)
        donation_options = category.amounts.all()
    else:
        return redirect('home')

    # Get pre-selected amount from query string
    preselected_amount = request.GET.get('amount', None)

    if request.method == "POST":
        amount_str = request.POST.get('amount', '').strip()
        if not amount_str:
            # fallback to preselected amount if not in POST
            amount_str = preselected_amount

        try:
            amount = Decimal(amount_str)
        except (InvalidOperation, TypeError):
            return render(request, 'trust/donation_form.html', {
                'campaign': campaign,
                'category': category,
                'donation_options': donation_options,
                'error': "Invalid donation amount.",
                'preselected_amount': amount_str
            })

        Donation.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            mobile=request.POST.get('mobile'),
            dob=request.POST.get('dob') or None,
            certificate_80g=request.POST.get('certificate_80g') == 'on',
            amount=amount,
            campaign=campaign,
            category=category,
        )
        return redirect('donation_success')

    return render(request, 'trust/donation_form.html', {
        'campaign': campaign,
        'category': category,
        'donation_options': donation_options,
        'preselected_amount': preselected_amount,
    })


def donation_success(request):
    return render(request, 'trust/donation_success.html')


# -----------------------
# About Us / Trustees
# -----------------------
def about_us(request):
    about = AboutUs.objects.first()
    stats = Stat.objects.all()
    return render(request, "trust/about_us.html", {"about": about, "stats": stats})


def board_of_trustees(request):
    trustees = Trustee.objects.all()
    return render(request, "trust/board_of_trustees.html", {"trustees": trustees})


# -----------------------
# Media
# -----------------------
def media(request):
    images = MediaItem.objects.filter(image__isnull=False).exclude(image="")
    videos = MediaItem.objects.filter(video__isnull=False).exclude(video="")
    return render(request, 'trust/media.html', {
        'images': images,
        'videos': videos,
    })


# -----------------------
# Impact Stories
# -----------------------
def impact_categories(request):
    categories = ImpactCategory.objects.all()
    return render(request, "trust/impact_categories.html", {"categories": categories})


def impact_category_detail(request, slug):
    category = get_object_or_404(ImpactCategory, slug=slug)
    stories = category.stories.all()
    return render(request, "trust/impact_category_detail.html", {
        "category": category,
        "stories": stories,
    })


# -----------------------
# Tenders
# -----------------------
def tender_notice_list(request):
    tenders = TenderNotice.objects.filter(is_active=True).order_by("-published_date")
    return render(request, "trust/tender_notice_list.html", {"tenders": tenders})


##Registerationform#
def register(request):
    villages = Village.objects.all()
    mandals = Mandal.objects.all()
    districts = District.objects.all()
    domains = Domain.objects.all()
    subdomains = SubDomain.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        adhar_number = request.POST.get("adhar_number")
        adhar_upload = request.FILES.get("adhar_upload")
        village_id = request.POST.get("village")
        mandal_id = request.POST.get("mandal")
        district_id = request.POST.get("district")
        subdomain_id = request.POST.get("subdomain")
        domain_id = request.POST.get("domain")
        mobile = request.POST.get("mobile")
        email = request.POST.get("email")
        qualification = request.POST.get("qualification")
        comment = request.POST.get("comment")

        try:
            village = Village.objects.get(id=village_id)
            domain = Domain.objects.get(id=domain_id)
            subdomain = SubDomain.objects.get(id=subdomain_id)
            mandal = Mandal.objects.get(id=mandal_id)
            district = District.objects.get(id=district_id)

            # 🔹 Check if domain is open
            if not subdomain.is_open:
                messages.error(request, f"Applications for {subdomain.title} are currently closed.")
                return redirect("register")

            # 🔹 Check if domain is full
            if subdomain.registration_set.count() >= subdomain.max_slots:
                messages.error(request, f"Slots are completed for {subdomain.title}. We will publish once slots are reopened.")
                return redirect("register")

            # 🔹 Create registration
            Registration.objects.create(
                name=name,
                adhar_number=adhar_number,
                adhar_upload=adhar_upload,
                village=village,
                mandal = mandal,
                district = district,
                subdomain = subdomain,
                domain=domain,
                mobile=mobile,
                email=email,
                qualification=qualification,
                comment=comment
            )
            messages.success(request, "Your Registration is successful!! We will contact you soon!!")
            return redirect("register")

        except Exception as e:
            messages.error(request, f"Error: {e}")

    return render(request, "trust/register.html", {
        "villages": villages,
        "domains": domains,
        "mandals": mandals,
        "districts": districts,
        "subdomains": subdomains
    })