# tests.py
from django.test import TestCase, RequestFactory
from django.urls import reverse
from .models import BranchDetails, SocietyDetails, shgdetails
from .forms import SHGDetailsForm, BranchDetailsForm, SocietyDetailsForm
from .views import (
    create_branch_view, update_branch_view,
    create_society_view, update_society_view,
    shg_details_form, get_group_names
)


class BranchDetailsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.url_create = reverse('create_branch')
        self.url_update = reverse('update_branch', args=[1])

    def test_create_branch_view(self):
        request = self.factory.post(self.url_create, {
            'branchcode': 12345,
            'branchname': 'Test Branch',
            # Provide values for other fields
        })
        response = create_branch_view(request)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission

        # Assert that the BranchDetails object was created
        self.assertTrue(BranchDetails.objects.filter(branchname='Test Branch').exists())

    def test_update_branch_view(self):
        branch = BranchDetails.objects.create(
            branchcode=12345,
            branchname='Test Branch',
            # Provide values for other fields
        )
        request = self.factory.post(self.url_update, {
            'branchcode': 54321,
            'branchname': 'Updated Branch',
            # Provide updated values for other fields
        })
        response = update_branch_view(request, branch.id)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission

        # Assert that the BranchDetails object was updated
        branch.refresh_from_db()
        self.assertEqual(branch.branchname, 'Updated Branch')


class SocietyDetailsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.url_create = reverse('create_society_view')
        self.url_update = reverse('update_society_view', args=[1])

    def test_create_society_view(self):
        request = self.factory.post(self.url_create, {
            'society_code': 12345,
            'society_name': 'Test Society',
            # Provide values for other fields
        })
        response = create_society_view(request)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission

        # Assert that the SocietyDetails object was created
        self.assertTrue(SocietyDetails.objects.filter(society_name='Test Society').exists())

    def test_update_society_view(self):
        society = SocietyDetails.objects.create(
            society_code=12345,
            society_name='Test Society',
            # Provide values for other fields
        )
        request = self.factory.post(self.url_update, {
            'society_code': 54321,
            'society_name': 'Updated Society',
            # Provide updated values for other fields
        })
        response = update_society_view(request, society.id)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission

        # Assert that the SocietyDetails object was updated
        society.refresh_from_db()
        self.assertEqual(society.society_name, 'Updated Society')


class SHGDetailsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.url_form = reverse('shg_details_form')
        self.url_group_names = reverse('get_group_names')

    def test_shg_details_form(self):
        request = self.factory.post(self.url_form, {
            'group_name': 'Test Group',
            # Provide values for other fields
        })
        response = shg_details_form(request)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission

        # Assert that the shgdetails object was created
        self.assertTrue(shgdetails.objects.filter(group_name='Test Group').exists())

    def test_get_group_names(self):
        request = self.factory.get(self.url_group_names, {'search_query': 'Test'})
        response = get_group_names(request)
        self.assertEqual(response.status_code, 200)  # Success response

        # Assert that the response contains the expected group names
        response_data = response.json()
        self.assertIn('Test Group', response_data['suggestions'])


class FormTestCase(TestCase):
    def test_shg_details_form(self):
        form_data = {
            'group_name': 'Test Group',
            # Provide values for other fields
        }
        form = SHGDetailsForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_branch_details_form(self):
        form_data = {
            'branchcode': 12345,
            'branchname': 'Test Branch',
            # Provide values for other fields
        }
        form = BranchDetailsForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_society_details_form(self):
        form_data = {
            'society_code': 12345,
            'society_name': 'Test Society',
            # Provide values for other fields
        }
        form = SocietyDetailsForm(data=form_data)
        self.assertTrue(form.is_valid())
