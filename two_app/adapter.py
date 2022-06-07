from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import get_object_or_404

from django.http import HttpResponse
from two_app.models import CustomUser, Customer, Shop
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):

        user = sociallogin.user

        if request.session["user_type"] == "shop":
            if Customer.objects.filter(user__email=user).exists():
                raise ImmediateHttpResponse(
                    HttpResponse('You already have a Customer account. You cannot signin using Shop Account'))
            pass

        if request.session["user_type"] == "customer":
            print("sassss")
            if Shop.objects.filter(user__email=user).exists():
                raise ImmediateHttpResponse(
                    HttpResponse('You already have a Shop account. You cannot signin using Customer Account'))
            pass
        pass


class AccountAdapter(DefaultAccountAdapter):

    def get_signup_redirect_url(self, request):

        user = self.request.user
        print('user', user)

        if request.session["user_type"] == "shop":
            customuser = CustomUser.objects.get(email=user.email)
            customuser.is_shop = True
            customuser.save()

            # At this timing, create a new Shop object.
            shop = Shop.objects.create(
                user=CustomUser.objects.get(email=user.email),
                description="First Shop Comment"
            )
            shop_id = shop.shopId
            shop.save()

            path = '/accounts/shop/{shopId}/'
            return path.format(shopId=shop_id)


        # Handling of parameters to the model when coming from the customer login page
        # and the path to be redirected.
        elif request.session["user_type"] == "customer":

            # If there is a corresponding user in Customuser to request.user,
            # set is_customer to True and save.
            customer_user = CustomUser.objects.get(email=user.email)
            customer_user.is_customer = True
            customer_user.save()

            # At this timing, create a new Customer object.
            customer = Customer.objects.create(
                user=CustomUser.objects.get(email=user.email),
                description="First Customer Comment"
            )
            customer.save()

            # To set the original path for each store, a value is retrieved from a preconfigured session.
            # Note that this session key is not given to the user coming from the shop login.
            shop_name = request.session["shop_name"]
            shop_id = request.session["shop_id"]

            path = '/accounts/customer/{shop_name}/{shop_id}'
            return path.format(shop_name=shop_name, shop_id=shop_id)

        else:
            user = CustomUser.objects.get(email=user.email)
            user.delete()
            return HttpResponse("This is an error related to session. The registered USER deleted.")


    def get_login_redirect_url(self, request):

        user = self.request.user
        print('user', user)
        # aaa = request.session['user_type']
        # print("aaa",aaa)
        if request.session['user_type'] == "shop":
            shop = get_object_or_404(Shop, user__email=user.email)
            shop_id = shop.shopId
            path = f'/accounts/shop/{shop_id}/'
            return path.format(shop_id=shop_id)


        # Handling of parameters to the model when coming from the customer login page
        # and the path to be redirected.
        # This method is not used at registration, but at login, so save is not performed.
        elif request.session["user_type"] == "customer":

            shop_name = request.session["shop_name"]
            shop_id = request.session["shop_id"]

            path = '/accounts/customer/{shop_name}/{shop_id}'
            return path.format(shop_name=shop_name, shop_id=shop_id)

        else:
            return HttpResponse('This is an error related to session.')