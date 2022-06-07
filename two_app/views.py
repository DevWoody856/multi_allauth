from allauth.account.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from two_app.forms import ShopNameForm
from two_app.models import CustomUser, Shop, Customer


class HomeView(LoginView):
    template_name = "two_app/index.html"

    # Retrieve all objects in Shop and list them on template.
    def get(self, request, *args, **kwargs):
        shops = Shop.objects.all()
        context = {
            'shops':shops
        }

        return render(request, self.template_name, context)


class ShopLogin(LoginView):
    template_name = 'two_app/shop-login.html'


def customer_login(request, shop_name, shopId):
    shop = get_object_or_404(Shop, shopId=shopId)

    context = {
        "shop":shop
    }

    return render(request, 'two_app/customer-login.html', context)


@login_required(redirect_field_name=None)
def shopProfile(request, shopId):

    user=request.user

    # This is Route guard.
    shop = get_object_or_404(Shop, user__email=user.email)
    # Exclude Shop user that come from other shop profiles and Customer users coming from the customer side
    if not shop.shopId == shopId or Customer.objects.filter(user__email=user.email).exists():
        return redirect('two_app:home')

    form = ShopNameForm()

    # Check if the current user is in the Shop model.
    # If not, add the content of the "no comment" here.
    if Shop.objects.filter(user__email=user.email).exists():
        text = Shop.objects.filter(user__email=user.email).values_list('description', flat=True).get()
    else:
        text = "no comment"

    context = {
        'shop': shop,
        'text': text,
        'form': form
    }

    template = "two_app/shop-profile.html"

    return render(request, template, context)


# This view is for creating a shop name.
# Only the variation part of the form is separated from the above view,
@login_required
def shopNameCreate(request, shopId):

    # Auth guard
    # following code is to prevent customer users from accessing this view directly.
    if Customer.objects.filter(user__email=request.user.email).exists():
        return redirect('two_app:home')

    form = ShopNameForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            shop_name = form.cleaned_data['shop_name']
            shop = Shop.objects.filter(user=request.user).get()
            shop.shop_name = shop_name
            shop.save()

            context = {
                "shop":shop
            }

        # Important: Replace the form part entirely with success.html.
        if request.htmx:
            return render(request, 'two_app/success.html', context)
    else:
        form = ShopNameForm()
        context = {
            "form": form,
        }

    return render(request, 'two_app/shop-profile.html', context)





@login_required(redirect_field_name=None)
def customer_profile(request, shop_name, shopId, *args, **kwqrgs):

    user=request.user
    shop_name_session = request.session["shop_name"]
    shop_id_session = request.session["shop_id"]

    # This is Auth guard.
    # Exclude come from other customer profiles and if there is an object in the shop model.
    if not shop_name_session==shop_name \
            or shop_id_session==shopId \
            or Shop.objects.filter(user__email=user.email).exists():

        return redirect('two_app:home')

    customer = get_object_or_404(Customer, user__email=user.email)

    context = {
        'customer':customer
    }
    template = "two_app/customer-profile.html"
    return render(request, template, context)

