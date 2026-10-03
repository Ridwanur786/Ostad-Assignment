from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from authentication.models import Profile


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.profile_url = reverse('profile')
        self.profile_update_url = reverse('profile_update')
        self.change_password_url = reverse('change_password')

        # Existing user for tests
        self.password = 'SecurePassword123!'
        self.user = User.objects.create_user(
            username='johndoe',
            email='john@example.com',
            password=self.password,
            first_name='John',
            last_name='Doe'
        )
        self.profile, _ = Profile.objects.get_or_create(user=self.user)
        self.profile.role = 'owner'
        self.profile.phone_number = '+8801700000000'
        self.profile.address = '123 Dhaka Ave'
        self.profile.save()

    def test_registration_success(self):
        """Test registering a new tenant user with full information."""
        response = self.client.post(self.register_url, {
            'username': 'newtenant',
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice@example.com',
            'role': 'tenant',
            'phone_number': '+8801811111111',
            'address': 'Flat 4B, Gulshan, Dhaka',
            'password': 'StrongPassword789!',
            'confirm_password': 'StrongPassword789!',
        })
        # After registration, user is redirected to profile
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.profile_url)

        # Check DB records
        user = User.objects.get(username='newtenant')
        self.assertEqual(user.email, 'alice@example.com')
        self.assertEqual(user.first_name, 'Alice')
        self.assertEqual(user.profile.role, 'tenant')
        self.assertTrue(user.profile.is_tenant)
        self.assertFalse(user.profile.is_owner)
        self.assertEqual(user.profile.phone_number, '+8801811111111')

    def test_registration_password_mismatch(self):
        """Test registration fails if passwords do not match."""
        response = self.client.post(self.register_url, {
            'username': 'mismatchuser',
            'first_name': 'Bob',
            'last_name': 'Jones',
            'email': 'bob@example.com',
            'role': 'tenant',
            'password': 'StrongPassword789!',
            'confirm_password': 'DifferentPassword789!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='mismatchuser').exists())

    def test_registration_duplicate_username_and_email(self):
        """Test registration prevents duplicate username and duplicate email."""
        # Duplicate username
        res1 = self.client.post(self.register_url, {
            'username': 'johndoe',
            'first_name': 'Duplicate',
            'last_name': 'User',
            'email': 'unique@example.com',
            'role': 'tenant',
            'password': 'StrongPassword789!',
            'confirm_password': 'StrongPassword789!',
        })
        self.assertEqual(res1.status_code, 200)

        # Duplicate email
        res2 = self.client.post(self.register_url, {
            'username': 'uniqueuser',
            'first_name': 'Duplicate',
            'last_name': 'Email',
            'email': 'john@example.com',
            'role': 'tenant',
            'password': 'StrongPassword789!',
            'confirm_password': 'StrongPassword789!',
        })
        self.assertEqual(res2.status_code, 200)

    def test_login_with_username(self):
        """Test logging in with username."""
        response = self.client.post(self.login_url, {
            'username_or_email': 'johndoe',
            'password': self.password,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.profile_url)

    def test_login_with_email(self):
        """Test logging in with email address instead of username."""
        response = self.client.post(self.login_url, {
            'username_or_email': 'john@example.com',
            'password': self.password,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.profile_url)

    def test_login_invalid_credentials(self):
        """Test login fails with incorrect password."""
        response = self.client.post(self.login_url, {
            'username_or_email': 'johndoe',
            'password': 'WrongPassword!',
        })
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """Test user logout."""
        self.client.login(username='johndoe', password=self.password)
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

    def test_profile_view_requires_login(self):
        """Test that unauthenticated users are redirected to login."""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(self.login_url))

    def test_profile_view_authenticated(self):
        """Test profile page displays owner details properly."""
        self.client.login(username='johndoe', password=self.password)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')
        self.assertContains(response, 'Property Owner')
        self.assertContains(response, '+8801700000000')

    def test_profile_update(self):
        """Test updating user first name, phone number, and address."""
        self.client.login(username='johndoe', password=self.password)
        response = self.client.post(self.profile_update_url, {
            'first_name': 'Johnny',
            'last_name': 'Doe Updated',
            'email': 'johnny@example.com',
            'role': 'tenant',
            'phone_number': '+8801999999999',
            'address': 'New Address Dhanmondi',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.profile_url)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Johnny')
        self.assertEqual(self.user.last_name, 'Doe Updated')
        self.assertEqual(self.user.email, 'johnny@example.com')
        self.assertEqual(self.user.profile.phone_number, '+8801999999999')
        self.assertEqual(self.user.profile.role, 'tenant')
        self.assertTrue(self.user.profile.is_tenant)

    def test_change_password(self):
        """Test changing user password."""
        self.client.login(username='johndoe', password=self.password)
        new_pwd = 'BrandNewPassword999!'
        response = self.client.post(self.change_password_url, {
            'old_password': self.password,
            'new_password1': new_pwd,
            'new_password2': new_pwd,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.profile_url)

        # Verify new password can be used to log in
        self.client.logout()
        login_res = self.client.post(self.login_url, {
            'username_or_email': 'johndoe',
            'password': new_pwd,
        })
        self.assertEqual(login_res.status_code, 302)
