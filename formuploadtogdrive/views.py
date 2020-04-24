import os

from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from oauth2client.client import OAuth2Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from GDrive.settings import BASE_DIR, upload_folder_id, team_drive_id
from configurationfile import listfiles as listconfigurationfile
from configurationfile import path as pathconfigurationfile
from .forms import UserForm
from .functions import dati_utente
from .models import User


# Carica su GDrive
def index(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            # Caricamento file in GDrive

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
            queryset = User.objects.filter(matricola=MATRICOLA)
            indice = len(queryset)

            filename = '{}_{}_{}_{}_{}.{}'.format(MATRICOLA, NOME, COGNOME, VERSIONE, indice, ext)

            path_file_to_upload_to_GDrive = os.path.join(path_dir_file, filename)

            file_to_upload = drive.CreateFile({"title": filename, 'parents': [{'id': upload_folder_id}]})

            file_to_upload.SetContentFile(path_file_to_upload_to_GDrive)

            file_to_upload.Upload(param={'supportsAllDrives': True})

            # Imposto i permessi per l'utente che carica il file

            file_to_upload.InsertPermission(
                {'type': 'user',
                 'value': 'l.calabro2@campus.unimib.it',
                 'role': 'reader'}, sendNotificationEmails=False)

            return HttpResponseRedirect(reverse("uploadok"))


    else:
        form = UserForm()

    return render(request, 'index.html', {'form': form})


# Carica su team drive
def index2(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            # Caricamento file in GDrive

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
            queryset = User.objects.filter(matricola=MATRICOLA)
            indice = len(queryset)

            filename = '{}_{}_{}_{}_{}.{}'.format(MATRICOLA, NOME, COGNOME, VERSIONE, indice, ext)

            path_file_to_upload_to_GDrive = os.path.join(path_dir_file, filename)

            file_to_upload = drive.CreateFile(
                {"title": filename, 'parents': [{"kind": "drive#fileLink", 'id': team_drive_id}]})

            file_to_upload.SetContentFile(path_file_to_upload_to_GDrive)

            # file_to_upload.Upload()
            file_to_upload.Upload(param={'supportsAllDrives': True})

            # Imposto i permessi per l'utente che carica il file
            try:
                file_to_upload.InsertPermission(
                    {'type': 'user',
                     'value': 'l.calabro2@campus.unimib.it',
                     'role': 'reader'}, sendNotificationEmails=False)
            except:
                pass

            return HttpResponseRedirect(reverse("uploadok2"))


    else:
        form = UserForm()

    return render(request, 'index.html', {'form': form})


def uploadok(request):
    return render(request, 'uploadok.html', {'msg': 'Dati caricati correttamente'})


def uploadok2(request):
    return render(request, 'uploadok2.html', {'msg': 'Dati caricati correttamente'})


def list_file_in_folder(request):
    path_credentials = pathconfigurationfile + "\\" + listconfigurationfile[0]

    with open(path_credentials) as f:
        YOUR_ACCESS_TOKEN_IN_JSON_FORMAT = f.readline()

    gauth = GoogleAuth()

    gauth.credentials = OAuth2Credentials.from_json(YOUR_ACCESS_TOKEN_IN_JSON_FORMAT)

    drive = GoogleDrive(gauth)

    file_list = drive.ListFile({'q': "'" + upload_folder_id + "' in parents and trashed=false"}).GetList()

    listafile = ""

    for file1 in file_list:
        # print('-title: %s, -id: %s, -sharedlink: %s' % (file1['title'], file1['id'], file1['alternateLink']))
        listafile += 'title: {}<br>id: {}<br>webContentLink: <a href="{}" target="_blank">webContentLink</a><br>sharedlink: <a href="{}" target="_blank">sharablelink</a><br><br>'.format(
            file1['title'], file1['id'],
            file1['webContentLink'], file1['alternateLink'])

        # print(file1.GetPermissions())

    return HttpResponse("<h1>Lista file GDrive:</h1><br>" + listafile)


def list_file_in_folder2(request):
    path_credentials = pathconfigurationfile + "\\" + listconfigurationfile[0]

    with open(path_credentials) as f:
        YOUR_ACCESS_TOKEN_IN_JSON_FORMAT = f.readline()

    gauth = GoogleAuth()

    gauth.credentials = OAuth2Credentials.from_json(YOUR_ACCESS_TOKEN_IN_JSON_FORMAT)

    drive = GoogleDrive(gauth)

    file_list = drive.ListFile(
        {'q': "trashed=false",
         'corpora': "teamDrive",
         'teamDriveId': team_drive_id,
         'includeTeamDriveItems': True,
         'supportsTeamDrives': True
         }).GetList()

    listafile = ""

    for file1 in file_list:
        # print('-title: %s, -id: %s, -sharedlink: %s' % (file1['title'], file1['id'], file1['alternateLink']))
        listafile += 'title: {}<br>id: {}<br>webContentLink: <a href="{}" target="_blank">webContentLink</a><br>sharedlink: <a href="{}" target="_blank">sharablelink</a><br><br>'.format(
            file1['title'], file1['id'],
            file1['webContentLink'], file1['alternateLink'])

        # print(file1.GetPermissions())

    return HttpResponse("<h1>Lista file Team Drive:</h1><br>" + listafile)
