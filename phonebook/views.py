from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string
from django.views.generic import TemplateView, ListView

from phonebook.forms import ContactForm, ContactSearchForm
from phonebook.models import Contact


class IndexView(TemplateView):
    template_name = 'phonebook/index.html'

    # saving contacts
def save_contact_form(request, form, template_name):
    data = dict()
    if request.method =='POST':
      if form.is_valid():
        form.save
        data['form_is_valid'] = True
        contacts = Contact.objects.all()
        data['html_contact_list']=render_to_string("phonebook/includes/partial_contact_list.html",
                                                   {'contacts':contacts}
                                                   )
    else:
        data['form_is_valid'] = False
        context = {'form': form}
        data ['html_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)
# create contact
def contact_create(request):
    if request.method =='POST':
        form = ContactForm(request.POST)
    else:
        form = ContactForm()
        return save_contact_form(request, form, 'phonebook/contact_form.html')

# update contact
def contact_update(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method =='Post':
        form = ContactForm(request.POST, instance=contact)
    else:
        form = ContactForm(request.POST, instance=contact)
        return save_contact_form(request, form, 'phonebook/contact_update.html')

#delete contact
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    data = dict()
    if request.method =='POST':
        contact.delete()
        data['form_is_valid'] = True
        contacts = Contact.objects.all()
        data['html_contact_list'] = render_to_string('phonebook/includes/partial_contact_list.html',
                                                     {'contacts' : contacts}
                                    )
    else:
        context = {'contact' : contact}
        data['html_form'] = render_to_string('phonebook/contact_delete.html', context, request=request,)
        return JsonResponse(data)

# Create CBV for listing the contacts
class ContactListView(ListView):
    context_object_name = 'contacts'
    model = Contact
    template_name = 'phonebook/contact_list.html'

    def get_queryset(self):
        queryset = super(ContactListView, self).get_queryset().order_by('-first_name')

        by_name = self.request.GET.get('name')
        by_phone = self.request.GET.get('phone')

        if by_phone and by_name:
            return queryset.filter(
                Q(first_name__contains=by_name) | Q(last_name__contains=by_name) | Q(phone_number__contains=by_phone)
            )
        if by_name:
            return queryset.filter(
                Q(first_name__contains=by_name) | Q(last_name=by_name)
            )
        if by_phone:
            return queryset.filter(
                phone_number__contains=by_phone
            )
        return queryset
    def get_context_data(self, **kwargs):
        cxt = super(ContactListView, self).get_context_data(**kwargs)
        cxt['search_form'] = ContactSearchForm()
        return cxt
















