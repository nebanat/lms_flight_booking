from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework import status

from . import services as file_service
# Create your views here.


class FileView(APIView):
    """
        File upload view
    """
    parser_class = (FileUploadParser,)

    def post(self, request, format=None):
        """
        post request to upload file
        :param request: request object
        :param format:
        :return:
        """
        file_ = request.data.get('file', None)
        return Response({
            'message': 'File uploaded successfully',
            'data': {
                'file_details': file_service.upload_file(request.user, file_)
            }
        }, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        """
        change uploaded file
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        file_ = request.data.get('file', None)
        file_service.remove_file(request.user)
        return Response({
            'message': 'File updated successfully',
            'data': {
                'file_details': file_service.upload_file(request.user, file_)
            }
        })

    def delete(self, request, *args, **kwargs):
        """
        delete uploaded file
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        file_service.remove_file(request.user)
        return Response({
            'message': 'File Deleted successfully',
        })

