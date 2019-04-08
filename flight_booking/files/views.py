import os
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework import status

from .serializers import FileSerializer
from .models import File
# Create your views here.


class FileView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, format=None):
        """

        :param request:
        :param format:
        :return:
        """
        file_ = request.data.get('file', None)
        file_serializer = FileSerializer(data=dict(user=request.user.id,
                                                   file=file_))
        file_serializer.is_valid(raise_exception=True)
        file_serializer.save()
        return Response({
            'message': 'File uploaded successfully',
            'data': {
                'file_details': file_serializer.data
            }
        }, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        file_ = request.data.get('file', None)
        file_exist = get_object_or_404(File, user=request.user)
        os.remove(file_exist.file.path)
        file_exist.delete()
        file_serializer = FileSerializer(data=dict(user=request.user.id,
                                                   file=file_))
        file_serializer.is_valid(raise_exception=True)
        file_serializer.save()
        return Response({
            'message': 'File updated successfully',
            'data': {
                'file_details': file_serializer.data
            }
        })

    def delete(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        file_exist = get_object_or_404(File, user=request.user)
        os.remove(file_exist.file.path)
        file_exist.delete()
        return Response({
            'message': 'File Deleted successfully',
        })

