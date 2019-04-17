from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.utils.six import BytesIO
from PIL import Image
import base64


User = get_user_model()


# "borrowed" from easy_thumbnails/tests/test_processors.py
def create_image(storage, filename, size=(100, 100), image_mode='RGB', image_format='PNG'):
    """
    Generate a test image, returning the filename that it was saved as.

    If ``storage`` is ``None``, the BytesIO containing the image data
    will be passed instead.
    """
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(base64.b64decode(data.read()))
    return storage.save(filename, image_file)


# Create your tests here.
class FileUploadViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email='laurel@gmail.com',
            username='tester',
            password='laurelsamplepassword'
        )
        self.token = Token.objects.create(user=self.user)
        self.base_url = '/api/v1/file/'
        self.image = create_image(None, 'avatar.png')

    def test_unauthorised_picture_upload(self):
        response = self.client.post(f'{self.base_url}', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('detail', None), 'Authentication credentials were not provided.')

    def test_unsuccessful_upload_without_picture(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(f'{self.base_url}', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['file'][0], 'This field may not be null.')
