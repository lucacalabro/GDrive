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
    # file caricati dalla stessa matricola

    # lista file nella cartella del file system
    lf = os.listdir(upload_to)

    # lista file senza estensione
    def get_matricola(T):
        return T.split('_')[0]

    # Lista matricole per ogni file(ci possono essere doppioni)
    lm = list(map(get_matricola, lf))

    # Lista fatta di matricole uguali alla matricola dello studente
    lm = [m for m in lm if m == MATRICOLA]

    # Contro quanti elementi ci sono ed assegno l'indice incrementando di 1
    indice = len(lm) + 1

    filename = '{}_{}_{}_{}_{}.{}'.format(MATRICOLA, NOME, COGNOME, VERSIONE, indice, ext)

    # return the whole path to the file
    return os.path.join(upload_to, filename)


class User(models.Model):
    first_name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=20, blank=False)
    # document = models.FileField(upload_to='documents/', blank=False)
    document = models.FileField(upload_to=path_and_rename, blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Utenti"
        models.verbose_name_plural = "Utenti"
        models.verbose_name = "Utente"
