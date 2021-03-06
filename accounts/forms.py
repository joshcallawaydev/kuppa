""" account forms """
from django import forms
from .models import UserAccount


class UserAccountForm(forms.ModelForm):
    """ user account form class """
    class Meta:
        """ meta class """
        model = UserAccount
        exclude = ('user',)

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_city': 'Town or City',
            'default_address_line_one': 'Street Address 1',
            'default_address_line_two': 'Street Address 2',
            'default_county': 'County',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True

        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'border-brown'

            self.fields[field].label = False
