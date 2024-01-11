from django.test import TestCase


import datetime

from django.utils import timezone

from catalog.forms import RenewBookModelForm

# Create your tests here.


class RenewBookModelFormTest(TestCase):
    def test_renew_form_date_field_label(self):
        form= RenewBookModelForm()
        self.assertTrue(form.fields['due_back'].label is None or form.fields['due_back'].label== 'due_back')


    def test_renew_form_date_field_help_text(self):
        form = RenewBookModelForm()
        self.assertEqual(form.fields['due_back'].help_text, 'Enter a date between now and 4 weeks (default 3).')

    def test_renew_form_date_in_past(self):
        date=datetime.date.today() - datetime.timedelta(days=1)
        form=RenewBookModelForm(data={'due_back': date})
        self.assertFalse(form.is_valid())


    def test_renew_form_date_max(self):
        date = timezone.localtime() + datetime.timedelta(weeks=4)
        form= RenewBookModelForm(data={'due_back': date})
        self.assertTrue(form.is_valid())