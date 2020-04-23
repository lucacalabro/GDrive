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

            # lista file nella cartella del file system
            lf = os.listdir(path_dir_file)

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

            file_to_upload = drive.CreateFile({"title": filename, 'parents': [{'id': upload_folder_id}]})
            # file_to_upload = drive.CreateFile({"title": filename, 'parents': [{'id': team_drive_id}]})

            file_to_upload.SetContentFile(path_file_to_upload_to_GDrive)

            # file_to_upload.Upload()
            file_to_upload.Upload(param={'supportsAllDrives': True})

            # Imposto i permessi per l'utente che carica il file
            #
            # Fonti:
            # https://developers.google.com/drive/api/v3/reference/permissions
            # https://developers.google.com/drive/api/v3/manage-sharing

            permission = file_to_upload.InsertPermission(

                {
                    "kind": "drive#permission",
                    # "id": drive['permissionId'],
                    "type": "user",
                    "value": "l.calabro2@campus.unimib.it",
                    "domain": "unimib.it",
                    "role": "reader",
                    'sendNotificationEmails': 'false'
                    # "allowFileDiscovery": False,
                    # "displayName": string,
                    # "photoLink": string,
                    # "expirationTime": datetime,
                    # "teamDrivePermissionDetails": [
                    #     {
                    #         "teamDrivePermissionType": "file",
                    #         "role": "reader",
                    #         "inheritedFrom": file_to_upload['id'],
                    #         "inherited": True
                    #     }
                    # ],
                    # "permissionDetails": [
                    #     {
                    #         "permissionType": "file",
                    #         "role": "reader",
                    #         "inheritedFrom": file_to_upload['id'],
                    #         "inherited": True
                    #     }
                    # ],
                    # "deleted": boolean
                }  # , sendNotificationEmails=False
            )

            # permission = file_to_upload.permissions().insert(fileId=file_to_upload['id'], body=new_permission).execute()

            # permissions = file_to_upload.GetPermissions()
            #
            # print(permissions)

            # Rimozione file dal file system
            # if os.path.exists(path_file_to_upload_to_GDrive):
            #     os.remove(path_file_to_upload_to_GDrive)
            # import shutil
            # shutil.move(path_file_to_upload_to_GDrive, "/"+filename)

            # print(drive.GetAbout())
            print(file_to_upload)
            file2 = drive.CreateFile({'id': file_to_upload['id']})
            print(file2)
            # print(file2.GetPermissions())
            # print(file_to_upload['parents'][0]['id'])
            # print(file_to_upload['id'])

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

            # lista file nella cartella del file system
            lf = os.listdir(path_dir_file)

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

            # file_to_upload = drive.CreateFile({"title": filename, 'parents': [{'id': upload_folder_id}]})
            file_to_upload = drive.CreateFile(
                {"title": filename, 'parents': [{"kind": "drive#fileLink", 'id': team_drive_id}]})

            file_to_upload.SetContentFile(path_file_to_upload_to_GDrive)

            # file_to_upload.Upload()
            file_to_upload.Upload(param={'supportsAllDrives': True})

            # Imposto i permessi per l'utente che carica il file
            #
            # Fonti:
            # https://developers.google.com/drive/api/v3/reference/permissions
            # https://developers.google.com/drive/api/v3/manage-sharing
            try:
                file_to_upload.InsertPermission(
                    {'type': 'user',
                     'value': 'l.calabro2@campus.unimib.it',
                     'role': 'reader'})
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
