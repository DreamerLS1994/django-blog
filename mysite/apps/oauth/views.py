from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ProfileForm
from django.contrib import messages
from mainapp.views import get_data

# Create your views here.

@login_required
def profile_view(request):
    g_carousels, g_settings, g_catalogues, g_tags, g_friendlinks, g_onetext = get_data()
    return render(request, 'oauth/profile.html', {'carousels': g_carousels, 'friendlinks': g_friendlinks,
                                                  'settings': g_settings,'catalogues': g_catalogues,
                                                  'tags': g_tags, 'one': g_onetext})


@login_required
def update_profile_view(request):
    if request.method == 'POST':
        # request.FILES  for upload files
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, '资料更新成功！')
            return redirect('oauth:account_profile')
    else:
        # POST
        form = ProfileForm(instance=request.user)

    g_carousels, g_settings, g_catalogues, g_tags, g_friendlinks, g_onetext = get_data()

    return render(request, 'oauth/update_profile.html', context={'form': form, 'carousels': g_carousels,
                                                                 'friendlinks': g_friendlinks, 'settings': g_settings,
                                                                 'catalogues': g_catalogues, 'tags': g_tags, 'one': g_onetext})

