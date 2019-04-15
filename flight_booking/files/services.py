import os
from django.shortcuts import get_object_or_404
from .serializers import FileSerializer
from .models import File


def upload_file(requestor, file_):
    """
     upload file to a file server
    :param requestor: user requesting(logged in user)
    :param file_:
    :return:
    """
    file_serializer = FileSerializer(data=dict(user=requestor.id,
                                               file=file_))
    file_serializer.is_valid(raise_exception=True)
    file_serializer.save()
    return file_serializer.data


def remove_file(requestor):
    """
    remove a user file upload
    :param requestor: user requesting(logged in user)
    :return:
    """
    file_exist = get_object_or_404(File, user=requestor)

    try:
        os.remove(file_exist.file.path)
    except OSError:
        pass

    file_exist.delete()
