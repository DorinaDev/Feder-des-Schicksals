import tkinter
import json

# Kapitel 1: Der Pfad der Mutigen

gesammelte_infos = {} # Speichert, welche Quellen bereits gefunden wurden
infos_gesammelt = 0 
fortschritt_wirt = 0 # 0 = Erstes Gespräch, 1 = Wirt sagt, komm später wieder, 2 = Wirt verrät tiefere Infos
fortschritt_fischer = 0  # 0 = Noch nicht getroffen, 1 = Auftrag erhalten, 2 = Aufgabe erledigt
truhe = {1: {"name": "Heilkräuter", "anzahl": 3, "beschreibung": "Kräuter, um Wunden zu heilen."}} # Startinhalt
inventar = {"Goldmünzen": {"anzahl": 10, "beschreibung": "Hiesige Währung"}} # Startinventar
waffen_inventar = {}
rüstung_inventar = {}
gegenstands_datenbank = {
    "Goldmünzen": {
        "beschreibung": "Hiesige Währung"
    }, 
    "Heilkräuter": {
        "beschreibung": "Kräuter um Wunden zu heilen."
    },
    "Karte": {
        "beschreibung": "Karte der umliegenden Dörfer."
    }
}
waffen_datenbank = {"Dolch": {"Schaden": 2, "Abwehr": 1}, "Schwert": {"Schaden": 5, "Abwehr": 2}, "Kampfstab": {"Schaden": 4, "Abwehr": 3}}
rüstung_datenbank = {"Gambison": {"Abwehr": 1, "Gewicht": 0}, "Leichtes Kettenhemd": {"Abwehr": 2, "Gewicht": 1}}

# Infos hinzufügen
def info_hinzufügen(key, beschreibung):
    global gesammelte_infos, infos_gesammelt

    if key not in gesammelte_infos:
        gesammelte_infos[key] = beschreibung
        infos_gesammelt += 1
        print("\nDu hast eine neue Information gesammelt!")
    else: 
        print("\nDiese Information hattest du bereits.")

    print(f"Bisher hast du {infos_gesammelt} Infos gesammelt.")

# Truhe öffnen + Gegenstand nehmen
def truhe_öffnen():
    global inventar
    global truhe

    if not truhe:
        print("Die Truhe ist leer.")
        return

    print("\nDu öffnest die Truhe und findest folgende Gegenstände:")
    for key, item in truhe.items():
        print(f"{key}. {item['name']} - {item['beschreibung']} (Anzahl: {item['anzahl']})")
    
        try:
            wahl_truhe = int(input("\nWelchen Gegenstand möchtest du nehmen? (Bitte die Zahl angeben.) "))

            if wahl_truhe == 0:
                print("Du schließt die Truhe.")
                return
            
            if wahl_truhe in truhe:
                gewählter_gegenstand = truhe[wahl_truhe]

                if gewählter_gegenstand["name"] in inventar:
                    inventar[gewählter_gegenstand["name"]]["anzahl"] += 1
                else:
                    inventar[gewählter_gegenstand["name"]] = gewählter_gegenstand.copy()
                    inventar[gewählter_gegenstand["name"]]["anzahl"] = 1
            
                # Anzahl in der Truhe verringern
                truhe[wahl_truhe]["anzahl"] -= 1
                print(f"Du hast {gewählter_gegenstand['name']} aus der Truhe genommen. ({inventar[gewählter_gegenstand['name']]['anzahl']}x im Inventar)")

                # Gegenstand aufgebraucht --> entfernen
                if truhe[wahl_truhe]["anzahl"] <= 0:
                    del truhe[wahl_truhe]
            else:
                print("Dieser Gegenstand existiert nicht.")

        except:
            print("Ungültige Eingabe. Bitte gib eine Zahl ein.")

# Einen Gegenstand aufnehmen
def gegenstand_finden(item, menge):
    global inventar
    global waffen_inventar
    global rüstung_inventar

    if item in inventar:
        inventar[item]["anzahl"] += menge
        print(f"Du hast {item} aufgenommen. Jetzt hast du {inventar[item]['anzahl']} davon in deinem Inventar.")
        return

    if item in waffen_datenbank:
        daten = waffen_datenbank[item]
        waffen_inventar[item] = {"name": item, **daten}
        print(f"Du hast die Waffe '{item}' aufgenommen.") 
        print("Wähle deine aktive Waffe während des Kampfes.")
        return

    if item in rüstung_datenbank:
        daten = rüstung_datenbank[item]

        if not rüstung_inventar:
            print(f"Du hast die Rüstung '{item}' bekommen. Du ziehst sie direkt an.")
            rüstung_inventar[item] = {"name": item, **daten}

        else:
            alte_rüstung = list(rüstung_inventar.keys())[0]
            print("Du kannst immer nur eine Rüstung am Körper tragen. Möchtest du deine jetzige Rüstung behalten oder die neue tragen?")
            print("Die andere geht verloren, wenn du eine neue wählst")
            print(f"1. Ich möchte die alte Rüstung '{alte_rüstung}' behalten.")
            print(f"2. Ich möchte die neue Rüstung '{item}' anlegen.")

            while True:
                try:
                    wahl = int(input("> "))
                
                    if wahl == 1:
                        print(f"Du behälst deine jetzige Rüstung '{alte_rüstung}' an.")
                        break

                    elif wahl == 2:
                        print(f"Du lässt deine jetzige Rüstung {alte_rüstung} zurück und schlüpfst in die neue.")
                        rüstung_inventar.clear()
                        rüstung_inventar[item] = {"name": item, **daten}
                        break

                    else:
                        print("Ungültige Eingaben. Bitte wähle 1. oder 2.")
                except ValueError:
                    print("Ungültige Eingabe. Bitte gib eine Zahl ein")
        return
    
    daten = gegenstands_datenbank.get(item, {"beschreibung": "Ein unbekannter Gegenstand."})
    inventar[item] = {"name": item, "anzahl": menge, **daten}
    print(f"Du hast {menge}x {item} gefunden! Jetzt hast du {inventar[item]['anzahl']}x davon.")

# Waffenkammer : Nach dem Gespräch mit dem König
def waffenkammer():
    print("\nDu trittst in die Waffenkammer ein.")
    print("In der Waffenkammer befinden sich verschiedene Waffen und Rüstungen.")
    print("Welche Waffe möchtest du wählen?")

    # Waffen zur Auswahl
    wahl = input("1. Dolch\n2. Schwert\n3. Kampfstab\nWähle (1-3): ")

    if wahl == '1':
        print("\nDu hast einen Dolch gewählt. Du bist schnell und beweglich.")
        gegenstand_finden("Dolch", 1)
        
    elif wahl == '2':
        print("\nDu hast ein Schwert gewählt. Du bist gut bewaffnet für den Kampf.")
        gegenstand_finden("Schwert", 1)

    elif wahl == '3':
        print("\nDu hast einen Kampfstab gewählt. Du bist gut bewaffnet für den Kampf.")
        gegenstand_finden("Kampfstab", 1)

    else:
        print("\nUngültige Wahl. Du musst eine der Optionen wählen.")
        waffenkammer()
    
    print("Nun bist du bereit, um dein Abenteuer zu bestreiten. Als nächstes solltest du dich im Dorf umhören.\nDu kehrst ins Dort zurück.")
    dorfübersicht()

# Schänke
def schänke():
    global fortschritt_wirt

    if fortschritt_wirt == 0:
        print("\nDu betrittst die Schänke. Der Raum ist erfüllt von Stimmengewirr und dem Geruch nach gebratenem Fleisch.")
        print("Am Tresen steht der Wirt, ein paar Dorfbewohner sitzen an den Tischen und unterhalten sich.")
    elif fortschritt_wirt == 1: 
        print("\nDie Schänke ist noch gut besucht, aber du weißt, dass du später wiederkommen sollst.")
    else:
        print("\nDie Schänke ist nun leerer als zuvor. Der Wirt lehnt sich entspannt an den Tresen und beobachtet dich neugierig.")

    while True:
        print("\nWas möchtest du tun?")
        if fortschritt_wirt == 0:
            print("1. Mit dem Wirt sprechen")
            print("2. Dich unauffällig umhören")
            print("3. Zurück ins Dorf")
        elif fortschritt_wirt == 1:
            print("1. Warten, bis die Schänke leer ist")
            print("2. Die Zeit nutzen und woanders nachforschen")
        else:
            print("1. Mit dem Wirt über das Geheimnis sprechen")
            print("2. Zurück ins Dorf")

        wahl = input("> ")

        if wahl == "1":
            if fortschritt_wirt == 0:
                gespräch_mit_wirt()
            elif fortschritt_wirt == 1:
                print("\nDu bestellst dir einen Krug Wein und wartest, bis die letzten Gäste gegangen sind...")
                print("Die Schänke wird leerer, und endlich kann der Wirt offen mit dir sprechen.")
                fortschritt_wirt = 2
                offenbarung_wirt()
            else: 
                offenbarung_wirt()
        elif wahl == "2":
            if fortschritt_wirt == 0:
                umhören()
            elif fortschritt_wirt == 1:
                print("Du nutzt die Zeit, um dich im Dorf umzusehen.")
                dorfübersicht()
            else: 
                dorfübersicht()
        elif wahl == "3" and fortschritt_wirt == 0:
            dorfübersicht()  
            break
        else:
            print("\nUngültige Eingabe, versuche es erneut.")

# Gespräch mit Wirt
def gespräch_mit_wirt():
    global fortschritt_wirt

    print("\nDer Wirt wischt mit einem Tuch über den Tresen und sieht dich neugierig an...")
    print("Wirt: 'Hast du Hunger, Grünschnabel?'")
    print("\nWas möchtest du antworten?")
    print("1. 'Ich bin der Auserwählte! Habt gefälligst mehr Respekt!'")
    print("2. 'Nur einen Krug Wein. Ich bin wegen der Gerüchte hier. \nHabt Ihr hier auch von dem Dorf gehört, von dem alle sprechen?'")
    print("3. Gespräch beenden")

    wahl_wirt = input("> ")

    if wahl_wirt == "1":
        print("\nDer Wirt lacht schallend und klopft dir auf die Schulter.")
        print("Wirt: 'Haha! Ein Spaßvogel! Hier, trink was, das hebt die Laune.'")
        schänke()
    elif wahl_wirt == "2":
        print("\nDer Wirt lehnt sich zu dir herüber und spricht mit gedämpfter Stimme.")
        print("Wirt: 'Aye, ich habe davon gehört... Aber sei vorsichtig, nicht jeder mag es, wenn man zu viel fragt.'")
        print("\nWas willst du tun?")
        print("1. 'Ich will mehr wissen! Erzählt mir alles.'")
        print("2. 'Danke für den Tipp. Ich frage woanders nach.'")

        wahl_gerüchte = input("> ")

        if wahl_gerüchte == "1":
            print("\nDer Wirt sieht sich um und flüstert: 'Dann komm später wieder, wenn weniger Leute hier sind.'")
            fortschritt_wirt = 1
        elif wahl_gerüchte == "2":
            print("\nDu verlässt die Theke und überlegst, wo du sonst Informationen bekommen kannst.")
        else:
            print("\nDer Wirt runzelt die Stirn. 'Was redest du da? Ich verstehe dich nicht.'")
        
        schänke()

    elif wahl_wirt == "3":
        print("\nDu verlässt den Tresen und suchst dir einen ruhigen Platz.")
        schänke()
    else:
        print("\nDer Wirt runzelt die Stirn. 'Was redest du da? Ich verstehe dich nicht.'")
        schänke()

# Die Infos vom Wirt nachdem die Schänke geschlossen ist
def offenbarung_wirt():
    global fortschritt_wirt

    print("\nWirt: 'Also gut Grünschnabel. Du willst also etwas über die Gerüchte hören, die hier im Dorf ihre Runde machen.'")
    print("'Es begann vor etwa drei Monden, als die Sonne immer stärker und die Hitze immer unerträglicher wurde.'\nEr verzog in leidiger Erinnerung das Gesicht.")
    print("'Der kleine Bach, der neben dem Dorf herdümpelt, versiegte. Es war einfach zu heiß. Die Ernten drohten zu vertrocknen.'")
    print("'Doch keine sieben Tage später änderte sich alles von heute auf morgen. Die Menschen gruben nach Wasser,\nweiß der Teufel, woher sie wussten, wo sie graben mussten, und stießen auf eine unterirdische Quelle.'")
    print("'Das allein hatte schon Aufsehen erregt, doch dann wurde das Vieh krank. Die Tiere siechten vor sich hin und es schien,\nals seien sie alle verloren.'")
    print("'Doch auch diese Katastophe konnten die Dorfbewohner abwenden. Einer der Männer wurde ausgesandt, um ein bestimmtes Kraut zu finden.'")
    print("'Niemand hatte je davon gehört. Die Krankheit der Tiere galt bisher als unheilbar. Drei Tage später kehrte der Mann zurück und alle Tiere genesen.'")
    print("'Wenn du mich fragst, Grünschnabel, geht da etwas nicht mit rechten Dingen zu. Es gibt noch weitere Gerüchte.\nAber das ist das, was ich dir sagen kann.")
    info_hinzufügen("wirt", "Der Wirt hat dir vor von dem Dorf erzählt, das auf wundersame Weise mehreren Katastrophen entgangen ist.")

    print("Der Wirt blickt dich abwartend an. Was möchtest du tun?")
    print("1. Du blickst ihm tief in die Augen und antwortest: 'Das klingt nach dem Geschätz von alten Waschweibern.'")
    print("2. Du nickst nachdenklich und sagst: 'Habt Dank, Wirt. Kennt ihr vielleicht den Namen des Dorfes?'")
    print("3. Gespräch beenden")

    wahl_wirt = input("> ")

    if wahl_wirt == "1":
        print("\nDer Wirt lacht schallend und klopft dir auf die Schulter.")
        print("Wirt: 'Haha! Ja, das habe ich auch gedacht. Die Leute reden viel wenn der Tag lang ist. Hab eine gute Nacht, Grünschnabel.'")
        dorfübersicht()
    elif wahl_wirt == "2":
        print("\nWirt: 'Ich kann dir nur die Gerüchte erzählen, die ich hier so zu Ohren bekomme.\n Aber es gibt da einen alten Fischer, der war schonmal dort.\nSein Name ist Thalin und er sitzt für gewöhnlich am Weiler. Er kann dir mehr sagen.'")
        print("Mehr ist aus dem Wirt wohl nicht heraus zu bekommen. Du kehrst also ins Dorf zurück.")
        fortschritt_wirt = 3
        dorfübersicht()
    elif wahl_wirt == "3":
        print("\nDu verabschiedest dich vom Wirt und verlässt die Schänke.")
        dorfübersicht()
    else:
        print("\nDer Wirt runzelt die Stirn. 'Was redest du da? Ich verstehe dich nicht.'")
        schänke()

# Umhören
def umhören():
    print("\nDu setzt dich unauffällig an einen Tisch und lauschst den Gesprächen der Dorfbewohner.")
    print("Sie reden über die schlechten Ernten und das geheimnisvolle Dorf in den Bergen.")
    print("Einer erwähnt eine seltsame Feder, die magisch sein soll...")
    info_hinzufügen("umhöhren", "Du hast in der Bar den Gästen gelauscht und von einer geheimnisvollen Feder erfahren.") 
    schänke()

# Der Weiler
def weiler():
    global fortschritt_wirt

    print("\nDu erreichst den Dorfweiler. Eine leichte Brise kräuselt die Wasseroberfläche des kleinen Sees.")
    
    if fortschritt_wirt < 3:
        print("Es ist ruhig hier, aber nichts scheint ungewöhnlich. Vielleicht solltest du später wiederkommen.")

    else:
        print("Ein alter Mann sitzt am Steg und starrt ins Wasser. Er wirkt, als könnte er eine Geschichte erzählen.")
    
    print("\nWas möchtest du tun?")
    print("1. Zurück ins Dorf")
    
    if fortschritt_wirt >= 3:
        print("2. Mit dem alten Mann sprechen")

    wahl = input("> ")

    if wahl == "1":
        dorfübersicht()
    elif wahl == "2" and fortschritt_wirt >= 3:
        fischer()
    else:
        print("\nUngültige Eingabe. Versuche es erneut.")
        weiler()

# Der Fischer
def fischer():
    global fortschritt_fischer

    if fortschritt_fischer == 0:
        print("\nEin alter Mann sitzt am Steg und starrt ins Wasser. Er sieht aus, als hätte er viele Geschichten zu erzählen.")
        print("1. Mit ihm sprechen")
        print("2. Weitergehen")

        wahl = input("> ")

        if wahl == "1":
            print("\nDer alte Mann sieht dich an und lächelt verschmitzt.")
            print("'Sie sagen, ich sei ein verrückter alter Narr. Aber ich weiß Dinge, die du nicht weißt.'")
            print("1. 'Erzählt mir, was ihr wisst.'")
            print("2. 'Ich habe keine Zeit für Rätsel.'")

            wahl_fischer = input("> ")

            if wahl_fischer == "1":
                print("\nDer alte Mann seufzt. 'Ich könnte dir etwas erzählen, aber meine Pfeife ist verschwunden. Vielleicht bringst du sie mir?'")
                fortschritt_fischer = 1
            else:
                print("\nDer alte Mann lacht. 'Dann geh weiter, Grünschnabel.'")

        dorfübersicht()
    
    elif fortschritt_fischer == 1:
        print("\nDer alte Mann wartet auf seine Pfeife.")
        dorfübersicht()

    elif fortschritt_fischer == 2:
        print("\n'Du hast mir meine Pfeife gebracht! Also gut, hör zu...'")
        print("Er erzählt dir den Namen des Dorfes.")
        info_hinzufügen("fischer", "Du hast vom Fischer den Namen des Dorfes erfahren, indem die seltsamen Dinge vor sich gehen.") 

# Die Marktstände
def marktstände():
    print("Du schlenderst unauffällig zu den Marktständen herüber.")
    print("Auf den provisorischen Tischen siehst du die Waren der Händler aufgebahrt.")
    print("Seidene Stoffe, köstlich anmutende Früchte, Fisch und Dörrfleisch fallen dir zuerst ins Auge.")
    print("Die Luft ist erfüllt vom Duft der Gewürze, von Kaffee und Tee.")
    print("Die meisten Händler sind in Verkaufsgespräche verwickelt und ausschweifend am gestikulieren.")
    print("Neben dir am Stand mit den Stoffen stehen zwei junge Frauen, sie unterhalten sich über ihre Kinder, während sie die Tuche befühlen.")
    print("Beim Fleisch und Fisch steht ein Mann, der ratlos dreinblickt. Verdrossen stämmt er die Hände in die Seiten.")
    print("Neben den Gewürzen steht eine alte Frau in viele Tücher gehüllt und wedelt den Geruch der Ware in Richtung ihrer Nase.")
    print("Beim Teestand siehst du einen dunkel gekleidete Gestalt. Sie lässt ihren Blick über die Ware wandern.")

    while True: 
        print("\nVielleicht kannst du hier etwas für die Gerüchte das Dorf betreffend herausbekommen. Wen möchtest du gerne ansprechen?")
        print("1. Die Mütter am Tuchstand.")
        print("2. Den Mann beim Fleisch und Fischhändler.")
        print("3. Die alte Frau bei den Gewürzen.")
        print("4. Die dunkel gekleidete Gestalt am Teestand.")
        print("5. Zur Dorfübersicht zurückkehren.")

        try:
            gesprächspartner = int(input("> "))
            if gesprächspartner == 1:
                print("Die Frauen blicken irritiert zu dir auf, als du ihr Gespräch unterbrichst, wenden sich dir aber bereitwillig zu.")
                print("Die Ältere der beiden Frauen beäugt dich kritisch, ehe sie mit dir spricht.")
                print("'Jeder hier kennt die Gerüchte. Die Menschen sind wütend.'")
                print("'Als letztes Jahr unser Vieh verhungert ist, hat der König nichts unternommen, um uns zu helfen.'")
                print("'Meine Kinder haben nachts in ihren Betten vor Hunger geweint. Das werde ich nicht vergessen.'")
                print("Die zweite Frau nickt zustimmend und wendet das Wort ebenfalls an dich.")
                print("'Wer sagt uns, dass es dieses Jahr nicht wieder passiert? Unser König kümmert sich einen feuchten Dreck um uns.'")
                print("'Er ist ein schwacher alter Nichtsnutz geworden.\nEs wird Zeit, dass wir uns um uns selbst kümmen und sei es nur für unsere Kinder.'")
                print("\nDie Frustration der beiden Mütter ist für dich beinahe greifbar. Aber der Zorn in ihren Augen verheißt nichts Gutes.")
                print("Schnell bedankest du dich für das Gespräch und wendest dich ab.")
                info_hinzufügen("frauen", "Du hast von den Frauen am Marktstand von den unzufriedenen Bürgern erfahren.")
            elif gesprächspartner == 2:
                print("Der Mann seufzt laut und schüttelt den Kopf, als du ihn ansprichst.")
                print("'Diese verdammten Händler haben die Preise erhöht! Letzte Woche war Fisch noch bezahlbar, jetzt kostet er das Doppelte.'")
                print("'Ich kann mir das nicht leisten, aber ohne Fleisch und Fisch wird meine Familie krank.'")
                print("Er runzelt die Stirn und beugt sich verschwörerisch zu dir.")
                print("'Ich sage dir was: Das ist kein Zufall. Ein paar Männer aus dem Dorf haben mit den Händlern verhandelt.'")
                print("'Einer dieser Dorfältesten soll hier seine Finger im Spiel haben. Und die Leute werden langsam sauer.'")
                print("Er schnaubt wütend und dreht sich wieder zu den Waren um, um Preise zu vergleichen.")
                info_hinzufügen("mann", "Du hast von einem Mann am Marktstand von den Preiserhöhungen erfahren.")
            elif gesprächspartner == 3:
                print("Die alte Frau nimmt einen tiefen Atemzug, als du sie ansprichst, und blinzelt langsam zu dir hinüber.")
                print("'Die Luft ist schwer. Etwas liegt in der Dunkelheit, das uns beobachtet.'")
                print("Sie senkt die Stimme und beugt sich leicht vor.")
                print("'Vögel fliegen nicht mehr über den Weiler. Die Hunde jaulen nachts, als ob sie den Tod wittern.'")
                print("'Etwas kommt auf uns zu. Und es wird nichts Gutes bringen.'")
                print("Sie schüttelt den Kopf und wendet sich wieder den Gewürzen zu, als wäre das Gespräch nie geschehen.")
                info_hinzufügen("alte_frau", "Eine alte Frau am Marktstand hat dir von einem drohenden Unheil erzählt.")
            elif gesprächspartner == 4:
                print("Die dunkel gekleidete Gestalt mustert dich, während sie einen Beutel Tee in der Hand dreht.")
                print("'Du bist nicht von hier. Und doch stellst du Fragen.'")
                print("Die Stimme ist ruhig, aber du spürst eine unterschwellige Anspannung.")
                print("'Hör gut zu: Nicht jeder hier akzeptiert den Zustand, in dem wir leben. Manche haben... Pläne.'")
                print("Die Gestalt hält inne, bevor sie einen letzten Blick auf dich wirft.")
                print("'Pass auf, mit wem du redest. Es könnte gefährlich sein, zu viel zu wissen.'")
                print("Ohne ein weiteres Wort dreht sich die Person um und verschwindet in der Menge.")
                info_hinzufügen("gestalt", "Eine verschleierte Gestalt hat sich an den Marktständen gewarnt, nicht zu viel zu fragen.")
            elif gesprächspartner == 5:
                print("Du verlässt die Marktstände und kehrst zum Dorfplatz zurück.")
                dorfübersicht()
            else:
                print("\nUngültige Eingabe, wähle eine Zahl zwischen 1 und 5.")
        except ValueError:
            print("\nUngültige Eingabe, bitte gib eine Zahl ein.")

# Die Kammer
def kammer():
    print("\nDu betrittst deine Kammer. Der Raum ist klein, aber zweckmäßig eingerichtet.")
    print("Ein einfaches Bett steht an der Wand, daneben ein kleiner Tisch mit einer Öllampe.")
    print("In der Ecke befindet sich eine alte Truhe, deren Schloss etwas angerostet wirkt.")
    print("Ein einziges Fenster lässt das fahle Mondlicht in den Raum strömen.")

    while True:
        print("\nWas möchtest du tun?")
        print("1. Forschritt speichern.")
        print("2. Truhe öffnen.")
        print("3. Kammer untersuchen.")
        print("4. Tagebuch öffnen.")
        print("5. Die Kammer verlassen.")

        wahl_kammer = int(input("> "))
        
        try:
            if wahl_kammer == 1:
                print("Dein Spielstand wird gespeichert.")
                spielstand_speichern()
            
            elif wahl_kammer == 2: 
                truhe_öffnen()
           
            elif wahl_kammer == 3:
                while True:
                    print("Was möchtest du untersuchen?")
                    print("1. Das Fenster.")
                    print("2. Das Bett.")
                    print("3. Den Tisch.")
                    print("4. Untersuchung beenden.")

                    untersuchung_kammer = int(input("> "))

                    try:
                        if untersuchung_kammer == 1:
                            print("\nDu trittst ans Fenster und blickst hinaus.")
                            print("Im Mondlicht erkennst du eine Gestalt, die über den Marktplatz eilt. Wer mag das sein?")
                            info_hinzufügen("geheimnisvolle_gestalt", "Du hast eine geheimnisvolle Gestalt von deinem Fenster aus beobachtet.")
                       
                        elif untersuchung_kammer == 2:
                            print("\nDu untersuchst das Bett. Die Matratze ist dünn, aber sauber.")
                            print("Unter dem Kopfkissen ertastest du ein Stück Papier.")
                            print("Du ziehst es hervor und entdeckst eine hastig geschriebene Notiz:")
                            print("'Nichts ist wie es scheint. Vertraue niemandem.'")
                            info_hinzufügen("notiz_kammer", "Du wurdest in einem Zettel gewarnt, dass nichts sei, wie es scheint.")
                        
                        elif untersuchung_kammer == 3:
                            print("\nDer Tisch ist aufgeräumt, doch auf der Holzplatte sind einige Kerben zu sehen.")
                            print("Neben der Öllampe liegt eine alte Karte. Darauf sind dieses Dorf und die umliegenden Dörfer zu sehen.") 
                            print("Vielleicht könnte sie nützlich sein?")
                            print("Du steckst die Karte ein.")
                            gegenstand_finden("Karte", 1)
                        
                        elif untersuchung_kammer == 4:
                            print("Du beendest deine Untersuchungen.")
                            break
                        
                        else:
                            print("\nUngültige Eingabe, wähle eine Zahl zwischen 1 und 5.")
                    except ValueError:
                        print("\nUngültige Eingabe, bitte gib eine Zahl ein.")
            
            elif wahl_kammer == 4:
                print("Du öffnest dein Tagebuch und siehst eine Zusammenfassung aller Informationen, die du bereits gesammelt hast.")
                print(f"Bisher hast du {infos_gesammelt} Infos gesammelt.")
                print("Deine Einträge: ")
                for beschreibung in gesammelte_infos.values():
                    print(f"- {beschreibung}")

            elif wahl_kammer == 5:
                print("Du verlässt die Kammer.")
                dorfübersicht()
                break
            
            else:
                print("\nUngültige Eingabe, wähle eine Zahl zwischen 1 und 5.")
        except ValueError:
            print("\nUngültige Eingabe, bitte gib eine Zahl ein.")

# Das Schloss
def schloss():
    global infos_gesammelt
    global gesammelte_infos

    print("Du hast dich im Dorf umgehört und kehrst nun zurück, um Valtheris Bericht zu erstatten.")
    print("Man geleitet dich in den Thronsaal, vorbei an riesigen steinernen Säulen, die dir das Gefühl geben, klein und unbedeutend zu sein.")
    print("Die beiden gerüsteten Wachen, die dich hergeführt haben, weichen zur Seite und geben den Blick frei auf den Thron.")
    print("Du erblickst Valtheris, der lässig auf dem Sitz des Herrsches ruht und dich mit seinem Blick zu durchbohren scheint.")
    print("Der großgewachsene Mann mit den langen schwarzen Haaren, die ihm offen wie Seide über seine Schultern fallen, mustert dich nachdenklich.")
    print("Valtheris: 'Du hast mir also die Informationen, die ich brauche, um unser Königreich wieder zu seinem alten Glanz zu verhelfen, beschafft?'")
    print("Was möchtest du antworten?")
    print("1. 'Ja, mein Herr, ich komme um Bericht zu erstatten.'")
    print("2. 'Verzeiht, aber ich habe noch nicht genügend Informationen zusammen.'")

    while True:
        try:
            bericht = int(input("> "))

            if bericht == 1: 
                print("Valtheris lächelt versöhnlich.")
                print("'So sprich, mein junger Freund. Was konntet Ihr herausfinden?'")
                print("Du berichtest Valtheris von der Unzufriedenheit unter den Bürgern...")
                print("...von dem geheimnisvollen Dorf, das in aller Munde zu sein scheint...")
                print("...von der magischen Feder, die irgendwie damit zusammenhängen soll...")
            
                if "geheimnisvolle_gestalt" in gesammelte_infos or "notiz_kammer" in gesammelte_infos:
                    print("Möchtest du Valtheris auch von den Warnungen erzählen, die du erhalten hast?")
                    print("1. Ja, unbedingt! Wenn es jemanden gibt, der dem Königshaus schaden will, sollte Valtheris es wissen.")
                    print("2. Nein, ich behalte diese Informationen lieber für mich. Ich traue Valtheris nicht.")

                    while True:
                        try:
                            warnungen = int(input("> "))

                            if warnungen == 1:
                                print("Du erzählst Valtheris alles.")
                                print("Für eine Weile schweigt der Hausmeier.")
                                print("Valtheris: 'Es ist wirklich bedauerlich, dass es jene gibt, die nicht auf ihren König vertrauen.'")
                                print("'Was auch immer diese Subjekte andeuten wollten, sollte nicht ungesühnt bleiben.'")
                                print("'Ich werde dem nachgehen lassen, aber für Euch habe ich eine andere Aufgabe.'")
                                print("'Ich will, dass Ihr dieses Dorf findet und diese magische Feder ausfindig macht.'")
                                print("'Sobald Ihr sie in Euren Besitz gebracht habt, kehrt zu mir zurück und überbringt sie mir.'")
                                print("Deine Zustimmung scheint hier nicht von Bedeutung zu sein, denn Valtheris winkt bereits den Wachen zu, um dich zu eskortieren.")
                                print("'Ihr seid entlassen.' Damit ist das Gespräch offenbar beendet.")
                                break

                            elif warnungen == 2: 
                                print("Dir ist nicht wohl bei der Sache, daher entscheidest du dich dagegen, die Warnungen zu erwähnen.")
                                print("Du räusperst dich, nachdem du deine Erzählungen beendet hast und Valtheris nickt.")
                                print("Valtheris: 'Gut. Ihr werdet Eurem Ruf gerecht. Es war offenbar die richtige Entscheidung, euch rufen zu lassen.'")
                                print("'Der Name des Dorfes ist mir bekannt. Es liegt nicht weit entfernt.'")
                                print("'Ich möchte, dass Ihr Euch dorthin begebt und mir diese magische Feder beschafft, zum Wohle des Volkes.'")
                                print("'Kehrt zu mir zurück, sobald sie sich in Eurem Besitz befindet.'")
                                break
                    
                            else:
                                print("Ungültige Eingabe, bitte gib eine Zahl von 1 bis 2 ein.")

                        except ValueError:
                            print("Ungültige Eingabe, bitte gib eine Zahl ein.")
                else:
                    print("Du berichtest ohne die Warnungen.")
                break
            
            elif bericht == 2: 
                print("Valtheris schnaubt.")
                print("'Nun gut, dann geht Eurer Wege und lasst mich wissen, sobald Ihr brauchbare Informationen für mich habt.'")
                print("Du kehrst zurück ins Dorf.")
                dorfübersicht()
                break

            else:
                print("Ungültige Eingaben, bitte gib eine Zahl zwischen 1 und 2 an.")

        except ValueError:
            print("Ungültige Eingabe, bitte gib eine Zahl ein.")

    print("Du hast das erste Level von 'Die Feder des Schicksals' abgeschlossen.")
    print(f"Deine Erfolge: \nDu hast {infos_gesammelt}/8 Informationen gesammelt.")

    if 2 < infos_gesammelt <= 5:
        print("Du hast die wichtigsten Informationen gesammelt und startest ins nächste Level. Auf ins Dorf!")

    elif 6 < infos_gesammelt <= 7:
        print("Du hast genügend Informationen gesammelt. Für deine weitere Reise erhältst du 1x Heilkräuter. Auf ins Dorf!")
        gegenstand_finden("Heilkräuter", 1)

    elif infos_gesammelt == 8:
        print("Du hast alle Informationen gesammelt. Für deine weitere Reise erhältst du einen Gambison (Abwehr: 1, Gewicht: 0).")
        gegenstand_finden("Gambison", 1)

    start_level_2()

# Dreh- und Angelpunkt: Dorfübersicht
def dorfübersicht():
    while True:
        print("\nDu befindest dich auf dem Dorfplatz. Von hier aus kannst du in verschiedene Richtungen aufbrechen:")
        print("1. Gehe zur Schänke")
        print("2. Besuche den Weiler")
        print("3. Tritt an die Marktständen")
        print("4. Kehre in deine Kammer ein")

        if "geheimnisvolle_gestalt" in gesammelte_infos:
            print("5. Die geheimnisvolle Gestalt verfolgen")

        elif all(info in gesammelte_infos for info in ["fischer", "frauen", "umhören"]):
            print("6. Erstatte Bericht im Schloss")

        try:
            ortswahl = int(input("> "))
            if ortswahl == 1:
                schänke()
            elif ortswahl == 2:
                weiler()
            elif ortswahl == 3:
                marktstände()
            elif ortswahl == 4:
                kammer()
            elif ortswahl == 5 and "geheimnisvolle_gestalt" in gesammelte_infos:
                print("Du siehst die geheimnisvolle Gestalt, die du aus dem Fenster deiner Kammer beobachtet hast plötzlich um die Ecke biegen.")
                print("Unauffällig schleichst du hinterher, während sie sich immer wieder umblickend durch die leeren Gassen huscht.")
                print("Als ihr auf diese Weise plötzlich vor der Wehrmauer ankommt. Wendet sich die Gestalt plötzlich zu dir um.")
                print("Jetzt erst kannst du ihr Gesicht erkennen. Es handelt sich um eine junge Frau, vielleicht Ende 20, mit honigblondem Haar.")
                print("Einzelne Strähnen, die sich scheinbar aus ihrem Zopf gelöst haben, umrahmen ihr sinnliches Gesicht, das mit der Kapuze ihrer Gugel bedeckt ist.")
                print("Ihre hellgrünen Augen fixieren dich – doch ihr Blick ist sanft.")
                print("Unbekannte Frau: 'Ich wusste, dass Ihr mir folgen würdet.'")
                print("Du willst dich herausreden und öffnest deinen Mund, um zu protestieren, doch mit einer Geste bringt sie sich zum Schweigen.")
                print("'Es ist wichtig, dass Ihr mir aufmerksam zuhört. Wir haben nicht viel Zeit.' Gehetzt blickt sie sich erneut um.")
                print("'Es gibt solche, die Euren Erfolg um jeden Preis sichern wollen – und solche, die genauso verzweifelt versuchen, Euch scheitern zu lassen.'")
                print("'Wie auch immer es um Euer Schicksal bestellt sein mag, nehmt meine Bitte an: Lasst Euch allein von Eurem Herzen leiten.'")
                print("'Nur Euer Herz wird Euch den wahren Weg weisen können. Wenn Ihr Eurem Herzen nicht vertraut, sind wir alle verdammt'")
                print("Du runzelst die Stirn. Die Worte der jungen Frau haben in dir tausende Fragen aufgeworfen.")
                print("Was tust du?")
                print("1. Ihr glauben und schweigend nicken.")
                print("2. Misstrauisch fragen: 'Wer seid Ihr überhaupt?'")

                wahl_gestalt = int(input("> "))

                try:
                    if wahl_gestalt == 1:
                        print("Die junge Frau nickt und wendet sich wieder um, binnen eines Wimperrnschlages ist sie zwischen den Häusern verschwunden.")
                    elif wahl_gestalt == 2:
                        print("Sie streicht eine blonde Strähne aus ihrem Gesicht.")
                        print("'Wir kennen uns schon lange und doch hast du mich noch nie gesehen. Je weniger du weißt, desto besser.'")
                        print("\nWie reagierst du?")
                        print("1. Weiter nachhaken: 'Das reicht mir nicht. Ich will Antworten!'")
                        print("2. Ihr einfach vertrauen und schweigen.")

                        zweite_wahl = int(input("> "))

                        if zweite_wahl == 1:
                            print("Die Frau seufzt und schüttelt den Kopf. 'Ich kann nicht mehr sagen. Bitte... vertraut mir einfach.'")
                        elif zweite_wahl == 2:
                            print("Du nickst langsam. Irgendetwas in ihrem Blick gibt dir das Gefühl, dass sie die Wahrheit sagt.")
                        else:
                            print("Du zögerst – doch da ist sie schon verschwunden.")
                except ValueError:
                    print("\nUngültige Eingabe, bitte gib eine Zahl ein.")

                print("Du bist dir nicht sicher, was die junge Frau dir mit ihren Worten sagen wollte, doch du hast das Gefühl, dass es wichtig war.")
                info_hinzufügen("auf_herz_hören", "Die geheimnisvolle Frau, hat dich gebeten auf dein Herz zu hören.")
                gesammelte_infos.pop("geheimnisvolle_gestalt", None)

            elif ortswahl == 6 and all(info in gesammelte_infos for info in ["fischer", "frauen", "umhören"]):
                schloss()

            else:
                print("\nUngültige Eingabe, wähle eine Zahl zwischen 1 und 4.")
        
        except ValueError:
            print("\nUngültige Eingabe, bitte gib eine Zahl ein.")

# Spielstand speichern
def spielstand_speichern():
    daten = {
        "inventar": inventar,
        "gesammelte_infos": gesammelte_infos,
        "infos_gesammelt": infos_gesammelt,
        "truhe": truhe,
        "fortschritt_wirt": fortschritt_wirt,
        "fortschritt_fischer": fortschritt_fischer
    }

    with open("spielstand.json", "w") as datei:
        json.dump(daten, datei, indent=4)

    print("\nDein Spielstand wurde erfolgreich gespeichert!")

# Spielstand laden
def spielstand_laden():
    global gesammelte_infos, infos_gesammelt, fortschritt_wirt, fortschritt_fischer, truhe, inventar, aktueller_ort
    
    try:
        with open("spielstand.json", "r") as datei:
            daten = json.load(datei)

        gesammelte_infos = daten.get("gesammelte_infos", {})
        infos_gesammelt = daten.get("infos_gesammelt", 0)
        fortschritt_wirt = daten.get("fortschritt_wirt", 0)
        fortschritt_fischer = daten.get("fortschritt_fischer", 0)
        truhe = daten.get("truhe", {})
        inventar = daten.get("inventar", {})

        print("\nDein Spiel wurde geladen. Du befindest dich in deiner Kammer.")

        kammer()

    except FileNotFoundError:
        print("\nKein gespeicherter Spielstand gefunden.")

# Hauptcode des 1. Levels
def start_game():
    print("Willkommen in der Welt von 'Die Feder des Schicksals'!")
    print("Du bist ein Abenteurer, der auf eine Quest geschickt wird, um ein uraltes Artefakt zu finden.")
    print("Doch nicht alles ist, wie es scheint. Sei gewarnt, junger Held.\nDeine Entscheidungen werden das Schicksal dieser Welt bestimmen und sie für alle Zeit verändern.")
    print("Bereite dich auf ein spannendes Abenteuer vor!\n")
    
    print("Du betrittst den Raum des mächtigen Valtheris, des königlichen Magiers. Er wartet auf dich und sieht dich ernst an.")
    print("\nValtheris: 'Ah, der Auserwählte... es ist gut, dass du gekommen bist. Die Schutzzauber des Königreichs schwächen sich.'")
    print("'Der alte König, nun schwach und hilflos, kann nichts mehr tun. Der Zauber, der das Land schützt, bröckelt, und mit ihm unsere Sicherheit.'")
    print("'Gerüchte haben sich verbreitet, ein abgelegenes Dorf hat überlebenswichtige Geheimnisse entdeckt, die den Zauber erneuern könnten.'")
    print("'Was auch immer sie verbergen, könnte der Schlüssel sein, die Magie des Landes zu retten... oder sie für immer zu zerstören.'")
    
    print("\nValtheris schaut dich eindringlich an.")
    print("Valtheris: 'Es gibt nur eine Frage, die du dir stellen musst... bist du bereit, für das Königreich und den Zauber des Landes zu kämpfen?'")
    
    antwort = input("1. 'Ja, ich werde dieses Artefakt finden.'\n2. 'Warum sollte ich dem König vertrauen?'\n\nWähle eine Antwort (1/2): ")

    if antwort == "1":
        print("\nValtheris lächelt weise.")
        print("'Gut, ich wusste, dass du die richtige Wahl treffen würdest. Du wirst von mir jegliche Unterstützung erhalten, die du brauchst. \nKomme jederzeit zu mir zurück, wenn du Fragen hast.'")
        print("'Du musst alles über dieses Dorf in Erfahrung bringen, was uns weiterhelfen könnte.")
        print("'Aber sei gewarnt, es wird viele Gefahren geben, und nicht jeder, dem du begegnest, wird ein Freund sein.'")
        print("\nDu fühlst dich gestärkt und bereit, deine Reise anzutreten. Doch ein flaues Gefühl bleibt in deinem Magen zurück.")
        start()

    else:
        print("\nValtheris schaut dich mit einer Mischung aus Enttäuschung und Erstaunen an.")
        print("'Du fragst dich, ob du dem König vertrauen solltest? Die Frage ist berechtigt.'")
        print("'Aber erinnere dich daran: Der König ist das Herz dieses Landes, und nur der wahre König kann das Land retten.'")
        print("'Du wirst dich entscheiden müssen, ob du dem König oder etwas anderem folgst.'")

def start():
    print("Du hast dich entschieden, die Mission anzunehmen und den Dorfgeheimnissen nachzugehen.")
    print("Mache dich bereit und wähle deine Ausrüstung.")
    waffenkammer()

# Hauptmenu
def hauptmenu():
    print("Willkommen zu deinem neuen Abenteuer 'Die Feder des Schicksals'!")
    print("Was möchtest du tun?")
    print("1. Das Abenteuer beginnen.")
    print("2. Meinen Spielstand laden.")
    print("3. Beenden.")

    while True:

        try:

            wahl_hauptmenu = int(input("> "))

            if wahl_hauptmenu == 1:
                start_game()
                return
            elif wahl_hauptmenu == 2:
                spielstand_laden()
                return
            elif wahl_hauptmenu == 3:
                print("Das Spiel wird nun beendet. Bis bald!")
                break
            else: 
                print("Bitte gib eine Zahl zwischen 1 und 3 ein.")
        
        except ValueError: 
            print("Ungültige Eingabe. Bitte gib eine Zahl ein.")

# Spiel starten
if __name__ == "__main__":
    hauptmenu()

# 2. Kapitel: Das Dorf
# Option einführen, bei Valtheris um Rat zu fragen.
# Die Entscheidung, ob man Valtheris von den Warnungen erzählt hat oder nicht, sollte eine Auswirkung haben, vielleicht wird jemand hingerichtet? 
# Während der Nachforschungen im Dorf gerät der Spieler zwischen die Fronten. Das Dorf wird von den Neidern der umliegenden Dörfer angegriffen
# Der Spieler wird mitten ins Chaos geschmissen: Brennende Scheune, maskierte Angreifer, Dorfbewohner die panisch fliehen.
# Der Spieler muss sich entscheiden: Will er den Dorfbewohnern helfen? Die Situation nutzen, um sich unbemerkt umzusehen? oder den Angreifern folgen, um zu sehen, was dahinter steckt?

def start_level_2():
    print("Hier beginnt Level 2.")