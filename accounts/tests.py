from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import CustomUser

class CustomUserTestCase(TestCase):
    """
    Test case for the CustomUser model.

    This test case includes various tests to ensure the correct behavior of the CustomUser model.
    """

    def setUp(self):
        self.user_data = {
            'username': 'test_user',
            'password': 'test_password',
            'role': 'user',
            'phone_number': '1234567890',
            'address': 'Test Address',
            'emergency_contact': 'Emergency Contact',
            'license_plate_number': 'ABC123'
        }
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_user_creation(self):
        """Test creation of a CustomUser instance."""
        self.assertEqual(self.user.username, self.user_data['username'])
        self.assertEqual(self.user.role, self.user_data['role'])
        self.assertEqual(self.user.phone_number, self.user_data['phone_number'])
        self.assertEqual(self.user.address, self.user_data['address'])
        self.assertEqual(self.user.emergency_contact, self.user_data['emergency_contact'])
        self.assertEqual(self.user.license_plate_number, self.user_data['license_plate_number'])

    def test_str_method(self):
        """Test the __str__ method of CustomUser."""
        self.assertEqual(str(self.user), self.user_data['username'])

    def test_blank_fields(self):
        """Test if blank fields are saved correctly."""
        blank_user_data = {
            'username': 'blank_test_user',
            'password': 'test_password'
        }
        blank_user = get_user_model().objects.create_user(**blank_user_data)
        self.assertEqual(blank_user.phone_number, '')  # Should be empty
        self.assertEqual(blank_user.address, '')  # Should be empty
        self.assertEqual(blank_user.emergency_contact, '')  # Should be empty
        self.assertEqual(blank_user.license_plate_number, '')  # Should be empty

    def test_role_choices(self):
        """Test if role choices are set correctly."""
        user = get_user_model().objects.create_user(username='user_test', password='test_password', role='user')
        admin = get_user_model().objects.create_user(username='admin_test', password='test_password', role='administrator')
        mod = get_user_model().objects.create_user(username='mod_test', password='test_password', role='moderator')

        self.assertEqual(user.role, 'user')
        self.assertEqual(admin.role, 'administrator')
        self.assertEqual(mod.role, 'moderator')

    def test_update_user_profile(self):
        """Test updating user profile fields."""
        self.user.phone_number = '9876543210'
        self.user.address = 'Updated Address'
        self.user.emergency_contact = 'Updated Emergency Contact'
        self.user.license_plate_number = 'XYZ789'
        self.user.save()

        updated_user = get_user_model().objects.get(id=self.user.id)
        self.assertEqual(updated_user.phone_number, '9876543210')
        self.assertEqual(updated_user.address, 'Updated Address')
        self.assertEqual(updated_user.emergency_contact, 'Updated Emergency Contact')
        self.assertEqual(updated_user.license_plate_number, 'XYZ789')

    def test_invalid_role_choice(self):
        """Test assigning an invalid role choice."""
        with self.assertRaises(ValueError) as context:
            get_user_model().objects.create_user(username='invalid_test_user', password='test_password', role='invalid_role')
        self.assertIn("Invalid role specified.", str(context.exception))

    def test_profile_picture_upload(self):
        """Test uploading a profile picture."""
        from django.core.files.uploadedfile import SimpleUploadedFile

        # Simulate image upload
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        self.user.profile_picture = image
        self.user.save()
        updated_user = get_user_model().objects.get(id=self.user.id)
        self.assertIn('profile_pictures/', updated_user.profile_picture.url)
