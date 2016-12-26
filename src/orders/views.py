from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView
from .forms import AddressForm, UserAddressForm
from .models import UserAddress, UserCheckout
# Create your views here.

class UserAddressCreateView(CreateView):
    form_class = UserAddressForm
    template_name = "forms.html"
    success_url = '/checkout/address'

    def get_checkout_user(self):
        user_check_id = self.request.session.get("user_checkout_id")
        user_checkout = UserCheckout.objects.get(id=user_check_id)
        return user_checkout

    def form_valid(self, form, *args, **kwargs):
        form.instance.user = self.get_checkout_user()
        return super(UserAddressCreateView, self).form_valid(form, *args, **kwargs)

class AddressSelectFormView(FormView):
    form_class = AddressForm
    template_name = "orders/address_select.html"


    def dispatch(self, *args, **kwargs):
        billing_address, shipping_address = self.get_addresses()

        if billing_address.count() == 0:
            messages.success(self.request, 'Please add a billing address before continuing')
            return redirect("user_address_create")
        elif shipping_address.count() == 0:
            messages.success(self.request, 'Please add a shipping address before continuing')
            return redirect("user_address_create")
        else:
            return super(AddressSelectFormView, self).dispatch(*args, **kwargs)

    def get_addresses(self, *args, **kwargs):
        user_check_id = self.request.session.get("user_checkout_id")
        user_checkout = UserCheckout.objects.get(id=user_check_id)

        billing_address = UserAddress.objects.filter(
            user=user_checkout,
            type='billing',
        )

        shipping_address = UserAddress.objects.filter(
            user=user_checkout,
            type='shipping',
        )

        return billing_address, shipping_address

    def get_form(self, *args, **kwargs):
        form = super(AddressSelectFormView, self).get_form(*args, **kwargs)

        billing_address, shipping_address = self.get_addresses()

        form.fields["billing_address"].queryset = billing_address
        form.fields["shipping_address"].queryset = shipping_address
        return form

    def form_valid(self, form, *args, **kwargs):
        self.request.session["billing_address_id"] = form.cleaned_data["billing_address"].id
        self.request.session["shipping_address_id"] = form.cleaned_data["shipping_address"].id
        return super(AddressSelectFormView, self).form_valid(form, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        return '/checkout/'