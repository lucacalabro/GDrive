import logging

import os

from oauth2client.client import OAuth2Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import google.oauth2.credentials

from documents import path as pathuploadsfile
from documents import listfiles as listuploadsfile
from configurationfile import path as pathconfigurationfile
from configurationfile import listfiles as listconfigurationfile

from django.shortcuts import redirect, render
from django.http import HttpResponse

from .forms import DocumentForm

import mimetypes





def upload_gdrive(request):
    # Apertura del file contenente le credenziali d'accesso aGDrive con l'utente di servizio serviziwebsi@unimib.it

    path_credentials = pathconfigurationfile + "\\" + listconfigurationfile[0]

    with open(path_credentials) as f:
        YOUR_ACCESS_TOKEN_IN_JSON_FORMAT = f.readline()

    gauth = GoogleAuth()

    gauth.credentials = OAuth2Credentials.from_json(YOUR_ACCESS_TOKEN_IN_JSON_FORMAT)

    drive = GoogleDrive(gauth)

    # Apertura del file da caricare su GDrive
    path_file_to_upload = pathuploadsfile + "\\" + listuploadsfile[0]

    # file_to_upload = drive.CreateFile(metadata={"title": listuploadsfile[0]})
    file_to_upload = drive.CreateFile()

    file_to_upload.SetContentFile(path_file_to_upload)

    file_to_upload.Upload()

    return HttpResponse(path_credentials + path_file_to_upload + YOUR_ACCESS_TOKEN_IN_JSON_FORMAT)
    # return HttpResponse(len(listuploadsfile[0]))
    # return HttpResponse(os.listdir())


# Carica un file sul file sitem del server nella cartella documents
def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            # *************************************

            # *************************************

            return redirect('uploadfile')
    else:
        form = DocumentForm()
    return render(request, 'upload.html', {
        'form': form
    })
