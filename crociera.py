from encodings import normalize_encoding
import csv
class Cabina:
    def __init__(self, codiceCabina, letti, ponte, prezzo):
        self._codiceCabina = codiceCabina
        self._letti = int(letti)
        self._ponte = int(ponte)
        self._prezzoBase = float(prezzo)
        self._disponibile = True
        self._codicePasseggero = None

    def prezzoFinale(self):
        return self._prezzoBase


class Standard(Cabina):

    def prezzoFinale(self):
        return self._prezzoBase

    def __str__(self):
        if self._disponibile:
            stato = "Disponibile"
        else:
            stato = f"Occupata da {self._codicePasseggero}"
        return f"{self._codiceCabina}: Standard | {self._letti} letti - Ponte {self._ponte} - Prezzo {self.prezzoFinale()} € - {stato}"



class Deluxe(Cabina):
    def __init__(self, codiceCabina, letti, ponte, prezzoBase, tipo):
        super().__init__(codiceCabina, letti, ponte, prezzoBase)
        self._tipo = tipo.strip()

    def prezzoFinale(self):
        prezzoFinale = self._prezzoBase * 1.2
        return prezzoFinale

    def __str__(self):
        if self._disponibile:
            stato = "Disponibile"
        else:
            stato = f"Occupata da {self._codicePasseggero}"
        return (f"{self._codiceCabina}: Deluxe | {self._letti} letti - Ponte {self._ponte} - Prezzo {self.prezzoFinale()} € - {stato} - {self._tipo}")


class Animali(Cabina):
    def __init__(self, codiceCabina, letti, ponte, prezzoBase, animali):
        super().__init__(codiceCabina, letti, ponte, prezzoBase)
        self._animali = int(animali)

    def prezzoFinale(self):
        prezzoFinale = self._prezzoBase * (1 + 0.1 * self._animali)
        return prezzoFinale

    def __str__(self):
        if self._disponibile:
            stato = "Disponibile"
        else:
            stato = f"Occupata da {self._codicePasseggero}"
        return (
            f"{self._codiceCabina}: Animali | {self._letti} letti - Ponte {self._ponte} - Prezzo {self.prezzoFinale()} € - {stato}"
            f" - Max Animali : {self._animali}")


class Passeggeri:
    def __init__(self, codicePasseggero, nome, cognome):
        self._codicePasseggero = codicePasseggero
        self._nome = nome
        self._cognome = cognome
        self._cabina = None


    def __str__(self):
        if self._cabina:
            return f"{self._codicePasseggero}: {self._nome} {self._cognome} - Cabina: {self._cabina._codiceCabina}"
        else:
            return f"{self._codicePasseggero}: {self._nome} {self._cognome} - Cabina: nessuna"



class Crociera:
    def __init__(self, nome):
        self._nome = nome
        self._listaCabine = []
        self._listaPasseggeri = []

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        if nome == "":
            raise ValueError("Nome non valido")
        self._nome = nome

    def carica_file_dati(self, file_path):
        try:
            with (open(file_path, "r", encoding="utf-8") as fileCrociera):
                csv_reader = csv.reader(fileCrociera)
                for riga in csv_reader:
                    if not riga:
                        continue
                    if riga[0].startswith("CAB"):
                        codiceCabina = riga[0].strip()
                        letti = int(riga[1])
                        ponte = int(riga[2])
                        prezzo = float(riga[3])

                        if len(riga) == 4: #standard
                            cabina = Standard(codiceCabina, letti, ponte, prezzo)

                        elif len(riga) == 5:
                            extra = riga[4]
                            if extra.isdigit(): #animali
                                cabina = Animali(codiceCabina, letti, ponte, prezzo, extra)
                            else: #deluxe
                                cabina = Deluxe(codiceCabina, letti, ponte, prezzo, extra)
                        else:
                            raise ValueError("Formato non valido")

                        self._listaCabine.append(cabina)

                    elif "P" in riga[0]: #passeggero
                        codicePasseggero = riga[0].strip()
                        nome = riga[1].strip()
                        cognome = riga[2].strip()
                        passeggero = Passeggeri(codicePasseggero, nome, cognome)
                        self._listaPasseggeri.append(passeggero)

                    else:
                        raise ValueError("Formato non valido")

        except FileNotFoundError:
            raise FileNotFoundError(f"File non valido {file_path}")


    def assegna_passeggero_a_cabina(self, codice_cabina, codice_passeggero):
        """Associa una cabina a un passeggero"""
        cabinaTrovata = None
        passeggeroTrovato = None

        for cabina in self._listaCabine:
            if cabina._codiceCabina == codice_cabina:
                if cabina._disponibile:
                    cabinaTrovata = cabina
                    break
                else:
                    raise ValueError(f"Cabina {codice_cabina} non disponibile")

        if cabinaTrovata is None:
            raise ValueError(f"Cabina con codice {codice_cabina} non torvata")

        for passeggero in self._listaPasseggeri:
            if passeggero._codicePasseggero == codice_passeggero:
                if passeggero._cabina is None:
                    passeggeroTrovato = passeggero
                    break
                else:
                    print(f"il passeggero con codice {codice_cabina} non libero")

        if passeggeroTrovato is None:
            raise ValueError(f"Passeggero con codice {codice_passeggero} non torvato")

        passeggeroTrovato._cabina = cabinaTrovata
        cabinaTrovata._codicePasseggero = passeggeroTrovato
        cabinaTrovata._disponibile = False




    def cabine_ordinate_per_prezzo(self):
        """Restituisce la lista ordinata delle cabine in base al prezzo"""
        return sorted(self._listaCabine, key= lambda cabina: cabina.prezzoFinale())


    def elenca_passeggeri(self):
        """Stampa l'elenco dei passeggeri mostrando, per ognuno, la cabina a cui è associato, quando applicabile """
        if not self._listaPasseggeri:
            print("Nessun passeggero registrato.")
            return

        for passeggero in self._listaPasseggeri:
            print(passeggero)



