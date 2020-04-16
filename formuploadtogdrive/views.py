import os

from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from oauth2client.client import OAuth2Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from GDrive.settings import BASE_DIR, upload_folder_id
from configurationfile import listfiles as listconfigurationfile
from configurationfile import path as pathconfigurationfile
from .forms import UserForm
from .functions import dati_utente

import time


# Create your views here.
def index(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            # Caricamento file in GDrive
            # time.sleep(10)

            # Apertura del file contenente le credenziali d'accesso aGDrive con l'utente di servizio serviziwebsi@unimib.it

            path_credentials = pathconfigurationfile + "\\" + listconfigurationfile[0]

            with open(path_credentials) as f:
                YOUR_ACCESS_TOKEN_IN_JSON_FORMAT = f.readline()

            gauth = GoogleAuth()

            gauth.credentials = OAuth2Credentials.from_json(YOUR_ACCESS_TOKEN_IN_JSON_FORMAT)

            drive = GoogleDrive(gauth)

            # Apertura del file da caricare su GDrive
            docfile = request.FILES['document']

            filename = docfile.name

            # estensione del file
            ext = filename.split('.')[-1]

            # Questi sono i dati letti da ESSE3
            dict_user = dati_utente()
            MATRICOLA = dict_user["MATRICOLA"]
            NOME = dict_user["NOME"]
            COGNOME = dict_user["COGNOME"]
            VERSIONE = dict_user["VERSIONE"]

            # cartella del filesystem in cui caricare il file
            path_dir_file = BASE_DIR + '/documents/'

            # Assegno un indice incrementale controllando i
            # file caricati dalla stessa matricola

            # lista file nella cartella del file system
            lf = os.listdir(path_dir_file)

            # return HttpResponse(path_dir_file)

            # lista file senza estensione
            def get_matricola(T):
                return T.split('_')[0]

            # Lista matricole per ogni file(ci possono essere doppioni)
            lm = list(map(get_matricola, lf))

            # Lista fatta di matricole uguali alla matricola dello studente
            lm = [m for m in lm if m == MATRICOLA]

            # Contro quanti elementi ci sono e ricavo l'ultimoindice
            # che corrisponde al file da caricare
            indice = len(lm)

            filename = '{}_{}_{}_{}_{}.{}'.format(MATRICOLA, NOME, COGNOME, VERSIONE, indice, ext)

            path_file_to_upload_to_GDrive = os.path.join(path_dir_file, filename)
            # path_file_to_upload_to_GDrive = os.path.join(path_dir_file, docfile.name)

            file_to_upload = drive.CreateFile({"title": filename, 'parents': [{'id': upload_folder_id}]})
            # return HttpResponse(path_file_to_upload_to_GDrive)
            file_to_upload.SetContentFile(path_file_to_upload_to_GDrive)

            file_to_upload.Upload()

            # Rimozione file dal file system
            # if os.path.exists(path_file_to_upload_to_GDrive):
            #     os.remove(path_file_to_upload_to_GDrive)
            # import shutil
            # shutil.move(path_file_to_upload_to_GDrive, "/"+filename)

            return HttpResponseRedirect(reverse("uploadok"))


    else:
        form = UserForm()

    return render(request, 'index.html', {'form': form})


def uploadok(request):
    return render(request, 'uploadok.html', {'msg': 'Dati caricati correttamente'})
