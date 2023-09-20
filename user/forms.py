from django import forms
from django.core.exceptions import ValidationError
from .models import CoinSettingsRegion, SetInterestedInRegion
from payments.models import SetPaymentMethodRegion


class CoinSettingsRegionForm(forms.ModelForm):
    class Meta:
        model = CoinSettingsRegion
        fields = ['title', 'countries']

    def clean(self):
        title = self.cleaned_data.get('title')
        countries = self.cleaned_data.get('countries')

        if title:
            dup_region = CoinSettingsRegion.objects.filter(title__iexact=title)
            if not self.instance._state.adding:
                dup_region = dup_region.exclude(id__in=[self.instance.id])
            if dup_region.count():
                raise ValidationError("Another region with the same title exists!")

        if countries:
            for country in countries.all():
                dup_region = CoinSettingsRegion.objects.filter(countries=country)
                if not self.instance._state.adding:
                    dup_region = dup_region.exclude(id__in=[self.instance.id])                
                if dup_region.count():
                    raise ValidationError("One of the selected countries belongs to another region! Country name: %s"%country)

        return self.cleaned_data


class PaymentGatewayRegionForm(forms.ModelForm):
    class Meta:
        model = SetPaymentMethodRegion
        fields = ['title', 'countries']

    def clean(self):
        title = self.cleaned_data.get('title')
        countries = self.cleaned_data.get('countries')

        if title:
            dup_region = SetPaymentMethodRegion.objects.filter(title__iexact=title)
            if not self.instance._state.adding:
                dup_region = dup_region.exclude(id__in=[self.instance.id])
            if dup_region.count():
                raise ValidationError("Another region with the same title exists!")

        if countries:
            for country in countries.all():
                dup_region = SetPaymentMethodRegion.objects.filter(countries=country)
                if not self.instance._state.adding:
                    dup_region = dup_region.exclude(id__in=[self.instance.id])
                if dup_region.count():
                    raise ValidationError("One of the selected countries belongs to another region! Country name: %s"%country)

        return self.cleaned_data


class UserInterestedInRegionForm(forms.ModelForm):
    class Meta:
        model = SetInterestedInRegion
        fields = ['title', 'countries']

    def clean(self):
        title = self.cleaned_data.get('title')
        countries = self.cleaned_data.get('countries')

        if title:
            dup_region = SetInterestedInRegion.objects.filter(title__iexact=title)
            if not self.instance._state.adding:
                dup_region = dup_region.exclude(id__in=[self.instance.id])
            if dup_region.count():
                raise ValidationError("Another region with the same title exists!")

        if countries:
            for country in countries.all():
                dup_region = SetInterestedInRegion.objects.filter(countries=country)
                if not self.instance._state.adding:
                    dup_region = dup_region.exclude(id__in=[self.instance.id])
                if dup_region.count():
                    raise ValidationError("One of the selected countries belongs to another region! Country name: %s"%country)

        return self.cleaned_data