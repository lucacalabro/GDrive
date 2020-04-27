import os
from django.db import models
from GDrive.settings import BASE_DIR
from .functions import dati_utente


# Create your models here.

# Serve a rinominare il file di cui fare l'upload
# e restituisce il path assegnandolo all'attributo upload_to
def path_and_rename(instance, filename):
    # Questi sono i dati letti da ESSE3
    dict_user = dati_utente()
    MATRICOLA = dict_user["MATRICOLA"]
    NOME = dict_user["NOME"]
    COGNOME = dict_user["COGNOME"]
    VERSIONE = dict_user["VERSIONE"]

    # cartella del filesystem in cui caricare il file
    upload_to = BASE_DIR + '/documents/'

    # estensione del file
    ext = filename.split('.')[-1]

    # Assegno un indice incrementale controllando i
    # file caricati per la stessa matricola
    indice = User.objects.filter(matricola=MATRICOLA).count() + 1

    filename = '{}_{}_{}_{}_{}.{}'.format(MATRICOLA, NOME, COGNOME, VERSIONE, indice, ext)

    # return the whole path to the file
    return os.path.join(upload_to, filename)



# Questi sono i dati letti da ESSE3
# Servono ad assegnare valori ai campi non mostrati nel form
dict_user_data = dati_utente()
MATRICOLA = dict_user_data["MATRICOLA"]
NOME = dict_user_data["NOME"]
COGNOME = dict_user_data["COGNOME"]
VERSIONE = dict_user_data["VERSIONE"]


class User(models.Model):
    field1 = models.CharField(max_length=20, blank=False)
    field2 = models.CharField(max_length=20, blank=False)
    matricola = models.CharField(default=MATRICOLA, max_length=20)
    nome = models.CharField(default=NOME, max_length=20)
    cognome = models.CharField(default=COGNOME, max_length=20)
    versione = models.CharField(default=VERSIONE, max_length=20)
    document = models.FileField(upload_to=path_and_rename, blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Utenti"
        models.verbose_name_plural = "Utenti"
        models.verbose_name = "Utente"


class Uploads(models.Model):
    title = models.CharField(max_length=500, blank=False)
    idfile = models.CharField(max_length=500, blank=False)
    webContentLink = models.CharField(max_length=500, blank=False)
    alternateLink = models.CharField(max_length=500, blank=False)
    index = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Uploads"
        models.verbose_name_plural = "Uploads"
        models.verbose_name = "Upload"


