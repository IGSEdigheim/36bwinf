#!/usr/bin/python3

def open_file(filename):
    schueler_liste = []
    with open(filename, "r") as inputfile:
        data = inputfile.readlines()
        for line in data:
            words = line.split()
            if words and words[0] == "+":
                for word in words[1:]:
                    schueler_liste[len(schueler_liste) - 1][1].add(word)
            elif words and words[0] == "-":
                for word in words[1:]:
                    schueler_liste[len(schueler_liste) - 1][2].add(word)
            elif words:
                schueler = ({words[0]}, set(), set())
                schueler_liste.append(schueler)
    return schueler_liste


def neuen_schueler_hinzufuegen(schueler, zimmer):
    # Steht der neue Schüler nicht auf der Menge-der-unerwünschten-Schüler des Zimmers?
    if not schueler[0] & zimmer[2]:
        # Steht kein Schüler des Zimmers auf der Menge-der-unerwünschten-Schüler des neuen Schülers?
        if not schueler[2] & zimmer[0]:
            print("Füge " + str(schueler[0]) + " dem Zimmer hinzu.")
            # neuerSchueler der Menge-der-Schüler-im-Zimmer hinzufügen
            zimmer[0].update(schueler[0])
            # Vereinige Menge-der-erwünschten-Schüler des Schülers und Menge-der-erwünschten-Schüler des Zimmers.
            zimmer[1].update(schueler[1])
            # Vereinige Menge-der-unerwünschten-Schüler des Schülers und Menge-der-unerwünschten-Schüler des Zimmers.
            zimmer[2].update(schueler[2])
            # Menge-der-erwünschten-Schüler um die Elemente, die in der Menge-der-Schüler-im-Zimmer sind bereinigen.
            zimmer[1].difference_update(zimmer[0])
            return True
        else:
            print("Unmöglich! " + str(schueler[0]) + " mag einen Schüler aus dem Zimmer nicht!")
    else:
        print("Unmöglich! Mindestens ein Schüler aus dem Zimmer mag " + str(schueler[0]) + " nicht!")
    return False


def schueler_auf_die_zimmer_verteilen(schueler_liste):
    zimmer_liste = []
    # solange es noch schüler gibt, die keinem Zimmer zugeordnet sind...
    while schueler_liste:
        neues_zimmer = schueler_liste.pop()
        zimmer_liste.append(neues_zimmer)
        print(str(neues_zimmer[0]) + " kommt in das neue Zimmer mit der Nummer " + str(len(zimmer_liste)) + ".")
        zimmer_voll = False
        while not zimmer_voll:
            zimmer_voll = True
            # Wenn die Menge-der-erwünschten-Schüler des Zimmer nicht leer ist...
            if neues_zimmer[1]:
                # Hole nächster Schüler aus der Menge-der-erwünschten-Schüler des Zimmers.
                likeschueler = neues_zimmer[1].pop()
                # Suche in der schueler_liste nach dem gewünschten Schüler des Zimmers.
                schueler_suche = [tSchueler for tSchueler in schueler_liste if likeschueler in tSchueler[0]]
                if schueler_suche:
                    # Nehme den nächsten Schüler falls möglich in das aktuelle Zimmer auf.
                    if neuen_schueler_hinzufuegen(schueler_suche[0], neues_zimmer):
                        # neuen Schueler aus schueler_liste löschen.
                        schueler_liste.remove(schueler_suche[0])
                    else:
                        return []
                zimmer_voll = False

            # Suche in der schueler_liste nach Schülern, deren Menge-der-erwünschten-Schüler eine Schnittmenge
            # mit der Menge-der-Schüler-im-Zimmer des aktuellen Zimmers hat.
            schueler_suche = [tSchueler for tSchueler in schueler_liste if neues_zimmer[0] & tSchueler[1]]
            if schueler_suche:
                # Nehme den nächsten Schüler falls möglich in das aktuelle Zimmer auf.
                if neuen_schueler_hinzufuegen(schueler_suche[0], neues_zimmer):
                    # neuer Schueler aus schueler_liste löschen.
                    schueler_liste.remove(schueler_suche[0])
                else:
                    return []
                zimmer_voll = False
    return zimmer_liste


if __name__ == "__main__":
    schueler_liste = open_file("zimmerbelegung3.txt")
    zimmer_liste = schueler_auf_die_zimmer_verteilen(schueler_liste)
    print("\nZimmerbelegung: ")
    for i, zimmer in enumerate([zimmer[0] for zimmer in zimmer_liste]):
        print("Zimmer " + str(i+1) + ": " + str(zimmer))
