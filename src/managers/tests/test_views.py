from django.test import TestCase

from django.urls import reverse


# Create your tests here.
class ViewsWithoutUsersAuthenticationTest(TestCase):
    """
    The tests for managers app views without users authentication.
    """

    def test_managers_home_view_without_authentication(self):
        manager_home_response = self.client.get(reverse('managers:home'))
        manager_update_account_response = self.client.get(reverse('managers:account_update'))

        self.assertEqual(manager_home_response.status_code, 404)
        self.assertEqual(manager_update_account_response.status_code, 404)

    def test_users_views_without_authentication(self):
        user_list_response = self.client.get(reverse('managers:user_list'))
        user_create_response = self.client.get(reverse('managers:user_create'))
        user_update_response = self.client.get(reverse('managers:user_update', args=[1]))
        user_delete_response = self.client.get(reverse('managers:user_delete', args=[1]))

        self.assertEqual(user_list_response.status_code, 404)
        self.assertEqual(user_create_response.status_code, 404)
        self.assertEqual(user_update_response.status_code, 404)
        self.assertEqual(user_delete_response.status_code, 404)

    def test_groups_views_without_authentication(self):
        group_list_response = self.client.get(reverse('managers:group_list'))
        group_update_response = self.client.get(reverse('managers:group_update', args=[1]))
        group_create_response = self.client.get(reverse('managers:group_create'))
        group_delete_response = self.client.get(reverse('managers:group_delete', args=[1]))

        self.assertEqual(group_list_response.status_code, 404)
        self.assertEqual(group_update_response.status_code, 404)
        self.assertEqual(group_create_response.status_code, 404)
        self.assertEqual(group_delete_response.status_code, 404)

    def test_departments_views_without_authentication(self):
        department_list_response = self.client.get(reverse('managers:department_list'))
        department_create_response = self.client.get(reverse('managers:department_create'))
        department_detail_response = self.client.get(reverse('managers:department_detail', args=[1]))
        department_update_response = self.client.get(reverse('managers:department_update', args=[1]))
        department_delete_response = self.client.get(reverse('managers:department_delete', args=[1]))

        self.assertEqual(department_list_response.status_code, 404)
        self.assertEqual(department_create_response.status_code, 404)
        self.assertEqual(department_detail_response.status_code, 404)
        self.assertEqual(department_update_response.status_code, 404)
        self.assertEqual(department_delete_response.status_code, 404)

    def test_projects_views_without_authentication(self):
        project_list_response = self.client.get(reverse('managers:project_list'))
        project_create_response = self.client.get(reverse('managers:project_create'))
        project_detail_response = self.client.get(reverse('managers:project_detail', args=[1]))
        project_update_response = self.client.get(reverse('managers:project_update', args=[1]))
        project_delete_response = self.client.get(reverse('managers:project_delete', args=[1]))

        self.assertEqual(project_list_response.status_code, 404)
        self.assertEqual(project_create_response.status_code, 404)
        self.assertEqual(project_detail_response.status_code, 404)
        self.assertEqual(project_update_response.status_code, 404)
        self.assertEqual(project_delete_response.status_code, 404)

    def test_workdays_views_without_authentication(self):
        workday_list_response = self.client.get(reverse('managers:workday_list'))
        workday_create_response = self.client.get(reverse('managers:workday_create'))
        workday_detail_response = self.client.get(reverse('managers:workday_detail', args=[1]))
        workday_update_response = self.client.get(reverse('managers:workday_update', args=[1]))
        workday_delete_response = self.client.get(reverse('managers:workday_delete', args=[1]))

        self.assertEqual(workday_list_response.status_code, 404)
        self.assertEqual(workday_create_response.status_code, 404)
        self.assertEqual(workday_detail_response.status_code, 404)
        self.assertEqual(workday_update_response.status_code, 404)
        self.assertEqual(workday_delete_response.status_code, 404)

    def test_invoices_views_without_authentication(self):
        invoice_list_response = self.client.get(reverse('managers:invoice_list'))
        invoice_create_response = self.client.get(reverse('managers:invoice_create'))
        invoice_delete_response = self.client.get(reverse('managers:invoice_delete', args=[1]))
        invoice_detail_response = self.client.get(reverse('managers:invoice_detail', args=[1]))
        invoice_update_response = self.client.get(reverse('managers:invoice_update', args=[1]))

        self.assertEqual(invoice_list_response.status_code, 404)
        self.assertEqual(invoice_create_response.status_code, 404)
        self.assertEqual(invoice_delete_response.status_code, 404)
        self.assertEqual(invoice_detail_response.status_code, 404)
        self.assertEqual(invoice_update_response.status_code, 404)

    def test_kala_views_without_authentication(self):
        kala_list_response = self.client.get(reverse('managers:kala_list'))
        kala_create_response = self.client.get(reverse('managers:kala_create'))
        kala_detail_response = self.client.get(reverse('managers:kala_detail', args=[1]))
        kala_update_response = self.client.get(reverse('managers:kala_update', args=[1]))
        kala_delete_response = self.client.get(reverse('managers:kala_delete', args=[1]))

        self.assertEqual(kala_list_response.status_code, 404)
        self.assertEqual(kala_create_response.status_code, 404)
        self.assertEqual(kala_detail_response.status_code, 404)
        self.assertEqual(kala_update_response.status_code, 404)
        self.assertEqual(kala_delete_response.status_code, 404)

    def test_ip_addresses_views_without_authentication(self):
        ip_address_list_response = self.client.get(reverse('managers:ip_address_list'))

        self.assertEqual(ip_address_list_response.status_code, 404)
