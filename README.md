# Software Engineering, Heizung – Brennersteuerung


## Genereller Plan

### Teilfunktionalitäten
- Temperaturmessung: <br>
Simulation eines Sensors zur Erfassung der Kesseltemperatur

- Sollwertregelung: <br>
Vergleich zwischen Ist- und Solltemperatur, Steuerung des Heizbetriebs

- Brennersteuerung: <br>
Steuerlogik: Ein-/Ausschalten des Brenners

- Sicherheitsüberwachung: <br>
Notabschaltung bei Fehlfunktionen (Übertemperatur, Sensorfehler)

- Benutzeroberfläche: <br>
Einfaches GUI zur Anzeige und Einstellung von Parametern

### Iterative Vorgehensweise
- Iteration 1
  - Temperaturmessung + Regelung + Brennerstatus
  - Ausgabe auf der Konsole
- Iteration 2
  - Einführung von Checks bzw. Fehlerbehandlung
  - Visualisierung
- Iteration 3
  - Vollständige UI
  - Tests


## Phasen des Software Engineering

### Requirement Engineering
- Funktionale Anforderungen
  - REQ-F01 - Umgebungstemperatursimulation <br>
    Das System simuliert die Umgebungstemperatur im Sekundentakt
  - REQ-F02 - Sollwerteingabe <br>
    Der Benutzer kann einen Sollwert eingeben
  - REQ-F03 - Automatisierte Brennerschaltung <br>
    Die Steuerlogik schaltet den Brenner bei Bedarf ein/aus
  - REQ-F04 - Sicherheitsmodul <br>
    Ein Sicherheitsmodul erkennt Grenzüberschreitungen
  - REQ-F05 - UI <br>
    Das UI zeigt Ist-, Soll- und Brennerstatus an
- Nicht-funktionale Anforderungen
  - REQ-NF01 - Universelle Lauffähigkeit <br>
    Die Software ist auf Windows und Linux lauffähig
  - REQ-NF02 - Reaktionszeit <br>
    Die Reaktionszeit auf Temperaturveränderung beträgt max. 2 s
  - REQ-NF03 - Testbarkeit <br>
    Die Software ist testbar mit Unit-Tests
  - REQ-NF04 - Sauberer Code <br>
    Lesbarer Code mit PEP8-Konformität

### Software Architektur
Schichtenarchitektur
- Präsentation: Ausgabe der Simulation
- Logik: Regelung/Steuerung
- Daten: Sensor-Simulation

![Klassendiagramm.png](documentation/Klassendiagramm.png)
![Sequenzdiagramm.png](documentation/Sequenzdiagramm.png)

### Software Design
Jede Hauptfunktionalität wird als Modul entworfen und getestet. <br>
Module: `sensor`, `control`, `safety`, `burner`, `ui`

![Moduldiagramm.png](documentation/Moduldiagramm.png)

### Implementierung
- Programmiersprache: Python
- Git für Versionskontrolle (öffentlich auf GitHub)
- Branches für Iterationen
- pytest für Unit-Tests (leichter als unittest)
- draw.io für Architektur/Diagramme

### Software Test
- Unit-Tests: Automatisiertes Testen einzelner Komponenten
- Integrationstests: Überprüfung des Zusammenspiels der Module.
