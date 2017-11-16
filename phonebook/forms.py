from django import forms
from phonebook.models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'location', 'emergency_contact']
        widgets= {
            'first_name' : forms.TextInput(attrs={'required': True, "placeholder": "Enter First Name"}),
            'last_name'  : forms.TextInput(attrs={'required': True, "placeholder": "Enter Last Name"}),
            'phone_number': forms.NumberInput(attrs={'required': True, "placeholder": "Enter Phone Number"}),
            'email': forms.EmailField(attrs={'required': True, "placeholder": "Enter Email Address"}),
            'location': forms.TextInput(attrs={'required': True, "placeholder": "Enter Location"}),
            'emergency_contact': forms.NumberInput(attrs={'required': True, "placeholder": "Enter Emergency Contact"}),

        }

def __init__(self, *args, *kwargs):
    super(ContactForm, self).__init__(*args, *kwargs)
    self.helper = FormHelper()
    self.helper.form_tag = False

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_qs = Contact.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This Email has already been registered")
        return email

class ContactSearchForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        required=False,
        help_text='Search by first name or last name'
    )
    phone = forms.IntegerField(
        required=False,
        help_text='Search by first name or last name'
    )

    def __init__(self, *args, **kwargs):
        super(ContactSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.layout = Layout(
            'name',
            'phone',
            Submit('Search', 'search', css_class='btn-default'),
        )
        self.helper.form_method = 'get'

    def get_queryset_filters(self):
        filters = {}
        if self.is_valid():
            name = self.cleaned_data.get('name')
            filters['name'] = name
