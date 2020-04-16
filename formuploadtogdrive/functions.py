# contiene funzioni di utilità generica

# restituisce una tupla con valori letti da ESSE3
def dati_utente():
    # Questi dati andranno valorizzati leggendo da Esse3
    MATRICOLA = "012345"
    NOME = "PINCO"
    COGNOME = "PALLINO"
    VERSIONE = "v1"

    return {"MATRICOLA": MATRICOLA, "NOME": NOME, "COGNOME": COGNOME, "VERSIONE": VERSIONE}
