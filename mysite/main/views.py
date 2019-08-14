from django.shortcuts import render, redirect
from .models import WP
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import NewUserForm
from .models import WP, WPworld, WPseries
from django.http import HttpResponse


# Create your views here.
def single_slug(request, single_slug):
    # first check to see if the url is in categories.

    worlds = [w.world_slug for w in WPworld.objects.all()]
    if single_slug in worlds:
        matching_series = WPseries.objects.filter(wp_world__world_slug=single_slug)
        series_urls = {}

        for m in matching_series.all():
            part_one = WP.objects.filter(wp_series__wp_series=m.wp_series).earliest("wp_published")
            series_urls[m] = part_one.wp_slug

        return render(request=request,
                      template_name='main/world.html',
                      context={"wp_series": matching_series, "part_ones": series_urls})

    wps = [t.wp_slug for t in WP.objects.all()]

    if single_slug in wps:
        this_wp = WP.objects.get(wp_slug=single_slug)
        wps_from_series = WP.objects.filter(wp_series__wp_series=this_wp.wp_series).order_by('wp_published')
        this_wps_idx = list(wps_from_series).index(this_wp)

        return render(request=request,
                      template_name='main/wp.html',
                      context={"wp": this_wp,
                               "sidebar": wps_from_series,
                               "this_tut_idx": this_wps_idx})
							   
    return HttpResponse(f"{single_slug} does not correspond to anything,")
	
def homepage(request):
    return render(request=request,
                  template_name='main/worlds.html',
                  context={"worlds": WPworld.objects.all})
				  

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})

    form = NewUserForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})
				  
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")
	
def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "main/login.html",
                    context={"form":form})
	