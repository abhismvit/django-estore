from django import forms
from django.forms.models import modelformset_factory

from .models import Variation, Category

class ProductFilterForm(forms.Form):
    q = forms.CharField(label='Search', required=False)
    category_id = forms.ModelMultipleChoiceField(
        label='Category',
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    max_price = forms.DecimalField(decimal_places=2, max_digits=12, required=False)
    min_price = forms.DecimalField(decimal_places=2, max_digits=12, required=False)


class VaraitionInventoryForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = [
            "title",
            "price",
            "sale_price",
            "inventory",
            "active"
        ]

VaraitionInventoryFormSet = modelformset_factory(Variation, form=VaraitionInventoryForm, extra=0)
