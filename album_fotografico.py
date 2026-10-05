def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    album = []
    try:
        # encoding utf-8 per leggere correttamente le lettere accentate
        with open(file_path, "r", encoding="utf-8") as file:
            next(file)  # salto la prima riga (intestazioni delle colonne)
            for riga in file:
                riga = riga.strip()  # tolgo spazi e gli a capo finali
                if riga == "":
                    continue  # ignoro righe vuote

                campi = [campo.strip() for campo in riga.split(",")] # tolgo spazi e divido con virgole
                if len(campi) != 5:
                    print(f"Riga ignorata (formato non valido): {riga}")
                    continue

                # prendo i campi uno alla volta, nell'ordine in cui compaiono nel file
                codice = campi[0]
                titolo = campi[1]
                autore = campi[2]
                try:
                    # converto mese e anno da testo a numeri interi
                    mese = int(campi[3])
                    anno = int(campi[4])
                except ValueError:
                    print(f"Riga ignorata (mese/anno non numerici): {riga}")
                    continue

                foto = [codice, titolo, autore, mese, anno]

                # cerco nell'album la voce [anno, lista_foto] relativa all'anno della foto
                foto_anno = None
                for voce_anno in album:
                    if voce_anno[0] == anno:
                        foto_anno = voce_anno[1]
                        break
                if foto_anno is None:
                    # quando trovo anno creo la voce [anno, lista_vuota]
                    foto_anno = [] # foto_anno è un riferimento alla lista dell'album
                    album.append([anno, foto_anno])
                foto_anno.append(foto) # facendo append la foto finisce direttamente dentro l'album

    except FileNotFoundError:
        # se il file non esiste restituisco None
        print(f"Errore: il file '{file_path}' non esiste.")
        return None

    print(f"Album caricato: {sum(len(voce[1]) for voce in album)} foto in {len(album)} anni.")
    return album


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    if mese < 1 or mese > 12: # controllo che il mese sia valido
        print("Errore: il mese deve essere compreso tra 1 e 12.")
        return None

    if cerca_foto(album, codice) is not None: # controllo che il codice non esista già
        print(f"Errore: esiste già una foto con codice {codice}.")
        return None

    foto = [codice, titolo, autore, mese, anno]

    # aggiorno il file e se fallisce non modifico l'album
    try:
        # verifico che il file esista
        with open(file_path, "r", encoding="utf-8") as file:
            contenuto = file.read()
        with open(file_path, "a", encoding="utf-8") as file:
            if contenuto and not contenuto.endswith("\n"): # aggiungo l'a capo se non c'è altrimenti la nuova foto sarebbe attaccata a quella prima
                file.write("\n")
            file.write(f"{codice},{titolo},{autore},{mese},{anno}\n")
    except FileNotFoundError:
        print(f"Errore: il file '{file_path}' non esiste.")
        return None

    # aggiorno la struttura dati, cerco l'anno nell'album
    foto_anno = None
    for voce_anno in album:
        if voce_anno[0] == anno:
            foto_anno = voce_anno[1]
            break
    if foto_anno is None: # se non c'è l'anno lo creo
        foto_anno = []
        album.append([anno, foto_anno])
    foto_anno.append(foto)

    return foto # riferimento alla foto appena aggiunta


def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""

    for anno, foto_anno in album:  # scorro tutti gli anni e, per ognuno, tutte le foto (doppio ciclo)
        for foto in foto_anno:
            if foto[0] == codice:  # codice della foto
                return f"{foto[0]}, {foto[1]}, {foto[2]}, {foto[3]}, {foto[4]}" # restituisco la stringa nel formato richiesto con i 5 campi della foto: codice, titolo, autore, mese, anno
    return None  # nessuna foto con quel codice


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    # cerco la voce [anno, lista_foto] dell'anno richiesto
    foto_anno = None
    for voce_anno in album:
        if voce_anno[0] == anno:
            foto_anno = voce_anno[1]
            break
    if foto_anno is None:
        return None # se l'anno non esiste non lo creo a differenza di prima

    titoli = [foto[1] for foto in foto_anno]  # ordino i titoli (foto[1] = titolo)
    return sorted(titoli, key=str.lower) # key=str.lower fa si che l'ordinamento sia indipendente da maiuscole/minuscole


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
