import datetime

from django.db import models
from django.utils import timezone


# class Contact(View):
#     def get(self, request):
#         puppy_form = PuppyForm()
#         return render(request, 'puppies/contact.html', {
#             'form': puppy_form
#         })
#
#     def post(self, request):
#         if settings.EMAIL_HOST and settings.CONTACT_EMAIL_TO_ADDRESS:  # are not None
#             puppy_form = ContactForm(request.POST)
#             if puppy_form.is_valid():
#                 from_email = 'appdev@rcc.uchicago.edu'
#                 subject = 'You have received a contact request from rsna.rcc.uchicago.edu'
#                 sender_email = puppy_form.cleaned_data['email']
#                 message = 'SENDER: %s %s (%s)\nLOCATION: %s, %s %s\nMESSAGE: %s' % \
#                           (puppy_form.cleaned_data['first_name'], puppy_form.cleaned_data['last_name'],
#                            puppy_form.cleaned_data['email'], puppy_form.cleaned_data['city'],
#                            puppy_form.cleaned_data['state'], puppy_form.cleaned_data['zip_code'],
#                            puppy_form.cleaned_data['message'])
#                 email = EmailMessage(
#                     subject=subject,
#                     body=message,
#                     from_email=from_email,
#                     reply_to=[sender_email],
#                     to=[settings.CONTACT_EMAIL_TO_ADDRESS]
#                 )
#                 email.send()
#                 return HttpResponse("Email Sent", status=200)
#             else:
#                 return HttpResponse("Email not send - invalid", status=400)
#         else:
#             return HttpResponse("EMAIL_HOST and/or CONTACT_EMAIL_TO_ADDRESS not configured in settings", status=501)


class Puppy(models.Model):
    """
    Puppy Model
    Defines the attributes of a puppy
    """
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    breed = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name + ' is added.'

    def __unicode__(self):
        return self.name

    def get_breed(self):
        return self.name + ' belongs to ' + self.breed + ' breed.'

    def was_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created_at <= now

        was_created_recently.admin_order_field = 'created_at'
        was_created_recently.boolean = True
        was_created_recently.short_description = 'Created recently?'
