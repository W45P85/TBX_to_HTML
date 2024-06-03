import os                                           # Betgriebssystem-spezifische Funktionen
import xml.etree.ElementTree as ET                  # Verarbeitung von XML-Daten
import tkinter as tk                                # GUI-Bibliothek
from tkinter import filedialog                      # Dateidialog-Funktionalität
from datetime import datetime                       # Datumsanzeige
import webbrowser 
from tkinter import *
from tkinter.ttk import *# Für Links in tkInter benötigt

class ScrollableFrame(tk.Frame):
    # Klasse für ein scrollbares Frame in der Gui
    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        # Canvas für Scrollbar erstellen
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        # Widgets anordnen
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw", tags="self.frame")

        # Event-Handler für Größenänderungen
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Scrollable Frame
        self.scrollable_frame = tk.Frame(self.frame, background="#ffffff")
        self.scrollable_frame.pack(fill="both", expand=True)

    # Event-Handler: Canvas-Größe ändern
    def on_canvas_configure(self, event):
            # Scrollable Frame an die Größe des Canvas anpassen
            canvas_width = event.width
            self.canvas.itemconfig("self.frame", width=canvas_width)

def open_github(event):
    webbrowser.open_new("https://github.com/W45P85/TBX_to_HTML")

def read_tbx(file_path, selected_columns):
    # Funktion zum Lesen einer TBX-Datei und Extrahieren von Daten
    tree = ET.parse(file_path)
    root = tree.getroot()

    term_dict = {}

    # Schritt 1: Durchlaufe jeden termEntry-Eintrag
    for entry in root.findall(".//termEntry"):
        concept_id = entry.get("id")
        lang_sets = entry.findall(".//langSet")

        terms_info = []

        # Schritt 2: Iteriere über alle <langSet> Tags unter dem aktuellen <termEntry>
        for lang_set in lang_sets:
            language = lang_set.get("{http://www.w3.org/XML/1998/namespace}lang", "")

            # Schritt 3: Iteriere über alle <termGrp> Tags unter dem aktuellen <langSet>
            for term_grp in lang_set.findall(".//termGrp"):
                term_info = {"term": "", "notes": {}, "language": language}

                # Schritt 4: Iteriere über alle <term> Tags unter dem aktuellen <termGrp>
                term = term_grp.find(".//term")
                if term is not None:
                    term_info["term"] = term.text

                # Schritt 5: Füge die Daten aus <termNote> Tags hinzu
                for term_note in term_grp.findall(".//termNote"):
                    note_type = term_note.get("type")
                    note_value = term_note.text
                    term_info["notes"][note_type] = note_value

                terms_info.append(term_info)

        # Schritt 6: Füge das Dictionary zum Dict hinzu
        if concept_id and terms_info:
            term_dict[concept_id] = terms_info

    return term_dict


# Funktion zum Konvertieren von TBX in HTML
def convert_tbx_to_html(file_path, html_file_path, selected_columns):
    term_dictionary = read_tbx(file_path, selected_columns)
    date = datetime.now().date()

    # Ersetze die alten Spaltennamen durch die neuen
    new_column_names = {
        'normativeAuthorization': 'Usage',
        'Benennungstyp|String': 'Term type',
        'Wortklasse|String': 'Word class',
        'Genus|String': 'Gender',
        'Definition|String': 'Definition',
        'Quelle|String': 'Source',
        'Anmerkung|String': 'Additional note',
        'Kontextbeispiel|String': 'Context example',
        'Termset|String': 'Term set'
    }

    # HTML-Inhalt erstellen
    html_content = f"""
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TBX in HTML konvertiert</title>
    <style>

    .tooltip {{
        position: relative;
    }}

    .tooltip .tooltiptext {{
        visibility: hidden;
        width: auto;
        background-color: #555;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 10000;
        bottom: 125%;
        left: 50%;
        margin-left: -60px;
        opacity: 0;
        transition: opacity 0.3s;
    }}

    .tooltip:hover .tooltiptext {{
        visibility: visible;
        opacity: 1;
    }}

    body {{
        font-family: 'Poppins', 'Helvetica Neue', Helvetica, Arial, sans-serif;
        background-color: #f8f9fa;
        margin: 0;
        text-align: center;
        padding: 20px;
    }}

    .container {{
        max-width: 1140px;
        margin: 0 auto;
        padding: 20px;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }}

    header {{
        text-align: left;
        display: flex;
        width: 100%;
        align-items: center;
        background-color: #000000;
        padding: 10px 20px;
        color: white;
        border-radius: 10px 10px 0 0;
    }}

    img {{
        max-width: 150px;
        padding: 5px;
        border-radius: 8px;
    }}
    
    h1 {{
        margin: 0;
        font-size: 2rem;
        color: white;
        padding-left: 10px;
    }}

    h2 {{
        color: #343a40;
        text-align: center;
        font-size: 1.75rem;
        margin-top: 20px;
    }}

    .search-container {{
        margin-top: 20px;
    }}

    p {{
        color: #6c757d;
        font-size: 1rem;
    }}
    
    small {{
        font-size: 0.875rem;
        margin-left: 1em;
        font-size: 16px;
    }}

    input[type="text"] {{
        text-align: center;
        padding: 10px;
        margin-bottom: 10px;
        border: 1px solid #ced4da;
        border-radius: 5px;
        width: calc(100% - 22px);
        max-width: 400px;
        margin-left: auto;
        margin-right: auto;
    }}

    button {{
        background-color: #007bff;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 1rem;
        transition: background-color 0.3s ease, transform 0.3s ease;
    }}

    button:hover {{
        background-color: #0056b3;
        transform: translateY(-2px);
    }}

    .hidden {{
        display: none;
    }}

    table {{
        border: 1px solid #dee2e6;
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        border-radius: 8px;
        overflow: hidden;
    }}

    th, td {{
        border: 1px solid #dee2e6;
        vertical-align: top;
        padding: 12px;
        text-align: left;
        border-bottom: 1px solid #dee2e6;
    }}

    th {{
        background-color: #009e8b;
        color: white;
    }}

    tr:nth-child(even) {{
        background-color: #f2f2f2;
    }}

    tr:hover {{
        background-color: #e9ecef;
    }}

    footer {{
        text-align: center;
        font-style: italic;
        margin: 20px 0;
        padding: 10px;
        background-color: #f8f9fa;
        border-top: 1px solid #dee2e6;
        color: #6c757d;
        border-radius: 0 0 10px 10px;
    }}

    .english-table {{
        display: none;
    }}
</style>


</head>
<header>
    <!-- <img src="img\logo.PNG" alt="Logo"> -->
    <h1>TERMINOLOGY Overview from: </h1>
    <small>{date}</small>
</header>
<body>

<p>Welcome to the terminology database. Here you will find a list of permitted and prohibited terms that should be used depending on the application.</p>
<p>Use the search field to search the table for terms.</p>
<p>In addition to the search function, the table can also be filtered using the drop-down menu.</p>
<p>There is a <a href="#legend">small legend at the bottom of the page</a> in case you have any initial questions.</p>

<div class="search-container">
    <input type="text" id="searchInput" placeholder="Search for terms" oninput="updateAutocomplete()">
    <div id="autocomplete" class="autocomplete-items"></div>
    <br />
    <br />
    <!-- Dropdown-Menü zur Auswahl des TermSet -->
        <label for="filterSelect">Select terminology set:</label>
        <select id="filterSelect">
            <option value="all">All</option>
            <option value="Standard">Default</option>
            <option value="ABC-Analyse">ABC-Analysis</option>
            <option value="LOGOMATE">LOGOMATE</option>
            <option value="INSTORE App">INSTORE App</option>
            <option value="RCC">COMMERCE Cloud</option>
            <option value="RPOS">POS</option>
            <option value="RETAIL">RETAIL</option>
            <option value="STATCONTROL">STATCONTROL Cloud</option>
            <option value="UCP">UCP</option>
            <option value="UI/UX">UI/UX</option>
            <option value="Handelterminologie">General Commerce and Logistics Terminology</option>
            <!-- Bei Bedarf weitere hinzufügen -->
        </select>
    <br />
    <br />
    <!-- Dropdown-Menü zur Auswahl der Sprache -->
        <label for="languageSelect">Select Language</label>
        <select id="languageSelect" onchange="filterTableLanguage()">
            <option value="" selected>All</option>
            <option value="en-us">English</option>
            <option value="de">Deutsch</option>
            <!-- Bei Bedarf weitere hinzufügen -->
        </select>
</div>

<table id="termTable">
    <tr>
        <th>Concept ID</th>
        <th>Language</th>
        <th>Term</th>
        <!-- Add headers here -->
"""

    for column in selected_columns:
        html_content += f"<th>{column}</th>\n"

    html_content += "</tr>\n"

    for concept_id, terms_info in term_dictionary.items():
        for term_info in terms_info:
            html_content += f"<tr>"
            html_content += f"<td>{concept_id}</td>"
            html_content += f"<td>{term_info['language']}</td>"
            html_content += f"<td>{term_info['term']}</td>"

            for column in selected_columns:
                # Verwende den ursprünglichen Spaltennamen für die Zuordnung des Inhalts
                original_column_name = next((key for key, value in new_column_names.items() if value == column), column)
                note_value = term_info["notes"].get(original_column_name, "-")
                html_content += f"<td>{note_value}</td>"

            html_content += "</tr>\n"

    html_content += """</table>

<script>
    var suggestionTimeout;

    // Funktion zum Aktualisieren der Autovervollständigung basierend auf Benutzereingaben
    function updateAutocomplete() {
        clearTimeout(suggestionTimeout);

        // Verzögere die Aktualisierung der Vorschläge um 500 Millisekunden
        suggestionTimeout = setTimeout(function () {
            var input, filter, table, tr, td, i, txtValue, found;
            input = document.getElementById('searchInput');
            filter = input.value.toUpperCase();
            table = document.getElementById('termTable');
            tr = table.getElementsByTagName('tr');

            // Array, um Concept-IDs der sichtbaren Zeilen zu speichern
            var visibleConceptIds = [];

            // Loop durch jede Zeile (überspringt die erste Zeile, die die Überschriften enthält)
            for (i = 1; i < tr.length; i++) {
                // Zeige die Zeile standardmäßig an
                tr[i].style.display = '';

                // Suche nur in der Spalte "Term" (Index 2)
                td = tr[i].getElementsByTagName('td')[2];
                if (td) {
                    txtValue = td.textContent || td.innerText;
                    if (txtValue.toUpperCase().indexOf(filter) > -1) {
                        found = true;

                        // Extrahiere die Concept-ID der gefundenen Zeile
                        var conceptId = tr[i].getElementsByTagName('td')[0].textContent || tr[i].getElementsByTagName('td')[0].innerText;

                        // Speichere die Concept-ID, wenn sie noch nicht gespeichert wurde
                        if (!visibleConceptIds.includes(conceptId)) {
                            visibleConceptIds.push(conceptId);
                        }
                    } else {
                        tr[i].style.display = 'none';
                    }
                }
            }

            // Wenn keine sichtbaren Zeilen vorhanden sind und die Sucheingabe nicht leer ist, zeige alle Zeilen mit den gespeicherten Concept-IDs
            if (visibleConceptIds.length > 0 && filter.trim() !== '') {
                for (i = 1; i < tr.length; i++) {
                    var conceptId = tr[i].getElementsByTagName('td')[0].textContent || tr[i].getElementsByTagName('td')[0].innerText;
                    if (visibleConceptIds.includes(conceptId)) {
                        tr[i].style.display = '';
                    } else {
                        tr[i].style.display = 'none';
                    }
                }
            }

            // Aktualisiere die Suchvorschläge
            updateSuggestions(filter);
        }, 500); // Warte 500 Millisekunden, bevor die Vorschläge aktualisiert werden
    }

    // Funktion zum Aktualisieren der Suchvorschläge basierend auf einem Filter
    function updateSuggestions(filter) {
        // Array für die Vorschläge initialisieren
        var suggestions = [];

        // Tabelle und Zeilen abrufen
        var termTable = document.getElementById('termTable');
        var tr = termTable.getElementsByTagName('tr');

        // Durchlaufe jede Zeile (überspringe die erste Zeile, die die Überschriften enthält)
        for (var i = 1; i < tr.length; i++) {
            var td = tr[i].getElementsByTagName('td');

            // Überprüfe jede Zelle in der Zeile
            for (var j = 0; j < td.length; j++) {
                var txtValue = td[j].textContent || td[j].innerText;

                // Überprüfe, ob der Begriff mit dem eingegebenen Filter beginnt
                if (txtValue.toUpperCase().startsWith(filter)) {
                    // Füge den gefundenen Begriff zu den Vorschlägen hinzu
                    suggestions.push(txtValue);
                    break; // Sobald ein passender Begriff gefunden wurde, breche die innere Schleife ab
                }
            }
        }

        // Anzeige der Vorschläge im Eingabefeld
        var autocompleteInput = document.getElementById('searchInput');
        if (suggestions.length > 0) {
            autocompleteInput.placeholder = suggestions[0].substring(filter.length);
        } else {
            autocompleteInput.placeholder = '';
        }
    }

// Funktion wird ausgeführt, wenn das Fenster vollständig geladen ist
window.onload = function() {
    // Funktionen aufrufen, um die Tabelle zu filtern, umzuschalten und Tooltips hinzuzufügen
    filterTable();            // filtert die Tabelle basierend auf Benutzereingaben
    toggleTable();            // schaltet die Legende um (zwischen de und en)
    addTooltipsFromTable()    // fügt Tooltips basierend auf den Daten in der Tabelle hinzu
    convertUrlsToLinks()      // konvertiert http:// und https:// Einträge in einen Link
};


// Funktion, die filterTable aufruft und für Kompatibilität bereitgestellt wird
function filterTableLanguage() {
    filterTable(); // Ruft die Hauptfilterfunktion filterTable() auf
}

// Hauptfilterfunktion, die die Tabelle basierend auf ausgewählter Sprache und Filteroption filtert
function filterTable() {
    // Ausgewählte Sprache und Filteroption aus den Dropdown-Listen abrufen
    var selectedLanguage = document.getElementById("languageSelect").value.toUpperCase();
    var selectedFilter = document.getElementById("filterSelect").value.toUpperCase();

    // Tabelle und Zeilen abrufen
    var table = document.getElementById("termTable");
    var rows = table.getElementsByTagName("tr");

    // Durchlaufe jede Zeile (überspringe die erste Zeile, die die Überschriften enthält)
    for (var i = 1; i < rows.length; i++) {
        // Zellen für Sprache und Filteroption abrufen
        var languageCell = rows[i].getElementsByTagName("td")[1].textContent.toUpperCase();
        var termsetCell = rows[i].getElementsByTagName("td")[11].textContent.toUpperCase();

        // Überprüfe, ob die Sprache und die Filteroption den ausgewählten Kriterien entsprechen
        var languageFilterPassed = selectedLanguage === "" || languageCell === selectedLanguage;
        var filterFilterPassed = selectedFilter === "ALL" || termsetCell.includes(selectedFilter);

        // Entscheide, ob die Zeile angezeigt oder ausgeblendet werden soll, basierend auf den Filterergebnissen
        if (languageFilterPassed && filterFilterPassed) {
            rows[i].classList.remove('hidden');
        } else {
            rows[i].classList.add('hidden');
        }
    }
}

    // Diese Funktion wird ausgeführt, wenn das DOM vollständig geladen ist
    document.addEventListener("DOMContentLoaded", function () {
        // Filter- und Sprachauswahl-Elemente aus dem DOM abrufen
        var filterSelect = document.getElementById('filterSelect');
        var languageSelect = document.getElementById('languageSelect');

        // Eventlistener hinzufügen, um auf Änderungen in der Filterauswahl zu reagieren und filterTable() aufzurufen
        filterSelect.addEventListener('change', function () {
            filterTable(); // filterTable() aufrufen, wenn sich die Filterauswahl ändert
        });

        // Eventlistener hinzufügen, um auf Änderungen in der Sprachauswahl zu reagieren und filterTable() aufzurufen
        languageSelect.addEventListener('change', function () {
            filterTable(); // filterTable() aufrufen, wenn sich die Sprachauswahl ändert
        });
    });

    // Funktion zum Umschalten zwischen deutscher und englischer Legende
    function toggleTable() {
         // Deutsche und englische Tabellen abrufen
        var germanTable = document.getElementById('german-table');
        var englishTable = document.getElementById('english-table');

        // Überprüfen, ob das Sprachumschalt-Checkbox-Feld aktiviert ist
        if (document.getElementById('language-toggle').checked) {
            // Englische Tabelle anzeigen, deutsche Tabelle ausblenden
            germanTable.style.display = 'table';
            englishTable.style.display = 'none';
        } else {
            // Deutsche Tabelle anzeigen, englische Tabelle ausblenden
            germanTable.style.display = 'none';
            englishTable.style.display = 'table';
        }
    }

// Funktion zum Hinzufügen von Tooltips basierend auf einer vordefinierten Tabelle
function addTooltipsFromTable() {
    // Tabelle mit den Tooltips
    // Syntax: "Wort", "Übersetzung", "Tooltip"

  var tooltipTable = [
    ["Hauptbenennung", "Main term designation", "This is the main term designation."],
    ["Substantiv", "Noun", "This is a noun."],
    ["Verb", "Verb", "This is a verb."],
    ["Adjektiv", "Adjective", "This is an adjective."],
    ["Adverb", "Adverb", "This is an adverb."],
    ["Synonym", "Synonym", "This is a synonym term."],
    ["Gemeinsprachlich", "Common language term", "This is a common language term"],
    ["Variante", "Variant", "This is a variant term."],
    ["Abkürzung", "Abbreviation", "This is a term abbreviation."],
    ["Kurzform", "Short form", "This is a short-form term."],
    ["Standardtext", "Standard usage", "This is standard usage term."],
    ["Femininum", "Feminine", "This is feminine."],
    ["Masculinum", "Masculine", "This is masculine."],
    ["Neutrum", "Neuter", "This is neuter."],
    ["Handelterminologie", "General Commerce and Logistics Terminology", "This is the General Commerce and Logistics Terminology."]
    // Hier können weitere Wörter und deren Übersetzungen eingefügt werden
];

  // Tabelle mit den Begriffen abrufen
  var termTable = document.getElementById("termTable");
  var cells = termTable.getElementsByTagName("td");

  // Durchlaufe jede Zelle in der Tabelle
  for (var i = 0; i < cells.length; i++) {
    var term = cells[i].innerText.trim();
    // Durchsuche die Tooltip-Tabelle nach dem aktuellen Begriff
    for (var j = 0; j < tooltipTable.length; j++) {
      if (tooltipTable[j][0] === term) { // Wenn der Begriff gefunden wird
        cells[i].classList.add("tooltip"); // Füge der Zelle die Klasse "tooltip" hinzu
        cells[i].innerHTML += '<span class="tooltiptext">' + tooltipTable[j][2] + '</span>'; // Füge den Tooltip hinzu
      }
    }
  }
}

function convertUrlsToLinks() {
    var table = document.getElementById("termTable");

    if (table) {
        for (var i = 0; i < table.rows.length; i++) {
            for (var j = 0; j < table.rows[i].cells.length; j++) {
                var cellContent = table.rows[i].cells[j].innerHTML;

                // Überprüfe, ob der Zelleninhalt eine URL enthält und "(translation)" nicht am Anfang steht
                if ((cellContent.includes("http://") || cellContent.includes("https://")) && !cellContent.includes("(translation)")) {
                    var link = document.createElement("a");
                    link.href = cellContent;
                    link.textContent = cellContent;
                    link.target = "_blank"; // Öffne den Link in einem neuen Fenster
                    table.rows[i].cells[j].innerHTML = '';
                    table.rows[i].cells[j].appendChild(link);
                } else if (cellContent.includes("(translation)")) {
                    // Teile den Zelleninhalt an der Position von "(translation)"
                    var parts = cellContent.split("(translation)");
                    // Erstelle einen neuen Link für den Teil vor "(translation)"
                    var linkBefore = document.createElement("a");
                    linkBefore.href = parts[0];
                    linkBefore.textContent = parts[0];
                    linkBefore.target = "_blank"; // Öffne den Link in einem neuen Fenster
                    // Erstelle einen Textknoten für den Teil nach "(translation)"
                    var textNodeAfter = document.createTextNode("(translation)" + parts[1]);
                    // Lösche den Zelleninhalt und füge den Link und den Textknoten ein
                    table.rows[i].cells[j].innerHTML = '';
                    table.rows[i].cells[j].appendChild(linkBefore);
                    table.rows[i].cells[j].appendChild(textNodeAfter);
                }
            }
        }
    } else {
        console.error("Tabelle nicht gefunden!");
    }
}

document.addEventListener('DOMContentLoaded', function() {
            var tableHeaders = document.querySelectorAll('#termTable th');
            tableHeaders.forEach(function(th) {
                th.style.position = 'sticky';
                th.style.top = '0';
                th.style.zIndex = '1000';
            });
        });

</script>


<h1 id="legend">Legende</h1>

<label for="language-toggle">German version</label>
    <input type="checkbox" id="language-toggle" onchange="toggleTable()">

    <table id="german-table">
        <!-- Deutsche Tabelle -->
        <thead>
            <tr>
                <th>Spaltenname</th>
                <th>Beschreibung</th>
                <th>Mögliche Werte</th>
                <!-- Weitere Spalten nach Bedarf -->
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Concept-ID</td>
                <td>Eindeutige Identifikationsnummer einer Termgruppe im Redaktionssystem SMC. Verschiedene Terme können zu einer Termgruppe gehören.</td>
                <td>Aufsteigende Nummerierung (z.B. concept-xxx)</td>
                <!-- Weitere Zeilen und Daten nach Bedarf -->
            </tr>
            <tr>
                <td>Language</td>
                <td>Jeweilige Sprache eines Terms innerhalb einer Termgruppe.</td>
                <td>de (Deutsch - Deutschland)<br>en_US (Englisch - USA)</td>
                <!-- Weitere Zeilen und Daten nach Bedarf -->
            </tr>
            <tr>
                <td>Usage</td>
                <td>Jeweilige Verwendungseinstufung eines Terms</td>
                <td>preferredTerm (Bevorzugter Begriff)<br>admittedTerm (Erlaubter Begriff/ Wörterbucheintrag)<br>deprecatedTerm (Gesperrter Begriff)</td>
                <!-- Weitere Zeilen und Daten nach Bedarf -->
            </tr>
            <tr>
                <td>Term type</td>
                <td>Jeweilige Art der Benennung eines Terms (z.B. Langform, Kurzform)</td>
                <td>Hauptbenennung<br>
                    Gemeinsprachliche Benennung<br>
                    Kurzform<br>
                    Abkürzung<br>
                    Standardtext<br>
                    Synonym<br>
                    Variante
                </td>
                <!-- Weitere Zeilen und Daten nach Bedarf -->
            </tr>
            <tr>
                <td>Word class</td>
                <td>Lexikalische Kategorie eines Terms (z.B. Verb)</td>
                <td>Substantiv: Nomen<br>Verb: Tätigkeitswort<br>Adjektiv: Eigenschaftswort<br>Adverb: Umstandswort</td>
                <!-- Weitere Zeilen und Daten nach Bedarf -->
            </tr>
            <tr>
                <td>Gender</td>
                <td>Grammatikalische Kategorie eines Terms (z.B. Männlich)</td>
                <td>Masculinum: Männlich<br>Femininum: Weiblich<br>Neutrum: Sächlich</td>
                <!-- Weitere Zeilen und Daten nach Bedarf -->
            </tr>
            <tr>
                <td>Definition</td>
                <td>Klar formulierte Erklärung oder Bedeutung des Terms.</td>
                <td>Freitexteingabe einer Definition eines Terms aus dem Redaktionssystem SMC</td>
                <!-- Weitere Zeilen und Daten nach Bedarf -->
            </tr>
            <tr>
                <td>Source</td>
                <td>Ursprung oder Referenz, woher der Term stammt.</td>
                <td>Freitexteingabe einer Quelle eines Terms aus dem Redaktionssystem SMC</td>
                <!-- Weitere Zeilen und Daten nach Bedarf -->
            </tr>
            <tr>
                <td>Additional note</td>
                <td>Zusätzliche Information für einen Term, insbesondere für Produkte.</td>
                <td>Freitexteingabe einer Quelle eines Terms aus dem Redaktionssystem SMC</td>
                <!-- Weitere Zeilen und Daten nach Bedarf -->
            </tr>
            <tr>
                <td>Context example</td>
                <td>Praktisches Beispiel, das den Term in einem Kontext zeigt.</td>
                <td>Freitexteingabe einer Quelle eines Terms aus dem Redaktionssystem SMC</td>
                <!-- Weitere Zeilen und Daten nach Bedarf -->
            </tr>
            <tr>
                <td>Term set</td>
                <td>Gruppierung des Terms in einem bestimmten produktspezifischen oder thematischen Satz oder Zusammenhang.</td>
                <td>Standard<br>
                    ABC-Analyse<br>
                    LOGOMATE<br>
                    INSTORE App<br>
                    RCC<br>
                    RPOS<br>
                    RETAIL<br>
                    STATCONTROL<br>
                    UCP<br>
                    UI/UX<br>
                    Handelsterminologie</td>
                <!-- Weitere Zeilen und Daten nach Bedarf -->
            </tr>
            <tr>
                <td>Select terminology set</td>
                <td>Das Dropdown-Menü "Select terminology set" ermöglicht es, spezifische Terminologiesets auszuwählen, um die angezeigten Begriffe in der Tabelle entsprechend zu filtern.</td>
                <td>Standard<br>
                    ABC-Analyse<br>
                    LOGOMATE<br>
                    INSTORE App<br>
                    RCC<br>
                    RPOS<br>
                    RETAIL<br>
                    STATCONTROL<br>
                    UCP<br>
                    UI/UX<br>
                    Handelsterminologie
                </td>
            </tr>
        </tbody>
    </table>

    <table id="english-table" class="english-table">
        <!-- Englische Tabelle (initial ausgeblendet) -->
        <thead>
            <tr>
                <th>Column Name</th>
                <th>Description</th>
                <th>Possible Values</th>
                <!-- Add more columns as needed -->
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Concept ID</td>
                <td>Unique identification number of a term group in the editorial system SMC. Different terms can belong to a term group.</td>
                <td>Ascending numbering (e.g., concept-xxx)</td>
                <!-- Add more rows and data as needed -->
            </tr>
            <tr>
                <td>Language</td>
                <td>Respective language of a term within a term group.</td>
                <td>de (German - Germany)<br>en_US (English - USA)</td>
                <!-- Add more rows and data as needed -->
            </tr>
            <tr>
                <td>Usage</td>
                <td>Respective classification of usage for a term.</td>
                <td>preferredTerm (Preferred Term)<br>admittedTerm (Allowed Term / Dictionary Entry)<br>deprecatedTerm (Deprecated Term)</td>
                <!-- Add more rows and data as needed -->
            </tr>
            <tr>
                <td>Term Type</td>
                <td>Respective type of naming for a term (e.g., long form, short form).</td>
                <td>Hauptbenennung: Main term destignation<br>
                    Gemeinschaftliche Benennung: Common language term<br>
                    Kurzform: Short-form designation<br>
                    Abkürzung: Term abbrevation<br>
                    Standardtext: Standard usage term<br>
                    Synonym: Synonym term<br>
                    Variante: Variant term
                </td>
                <!-- Add more rows and data as needed -->
            </tr>
            <tr>
                <td>Word Class</td>
                <td>Lexical category of a term (e.g., Verb).</td>
                <td>Substantiv: Noun<br>Verb: Verb<br>Adjectiv: Adjective<br>Adverb: Adverb</td>
                <!-- Add more rows and data as needed -->
            </tr>
            <tr>
                <td>Gender</td>
                <td>Grammatical category of a term (e.g., Masculine).</td>
                <td>Masculinum: Masculine<br>Femininum: Feminine<br>Neutrum: Neuter</td>
                <!-- Add more rows and data as needed -->
            </tr>
            <tr>
                <td>Definition</td>
                <td>Clearly formulated explanation or meaning of the term.</td>
                <td>Free text entry of a definition of a term from the editorial system SMC</td>
                <!-- Add more rows and data as needed -->
            </tr>
            <tr>
                <td>Source</td>
                <td>Origin or reference from where the term comes.</td>
                <td>Free text entry of a source of a term from the editorial system SMC</td>
                <!-- Add more rows and data as needed -->
            </tr>
            <tr>
                <td>Additional Note</td>
                <td>Additional information for a term, especially for products.</td>
                <td>Free text entry of a source of a term from the editorial system SMC</td>
                <!-- Add more rows and data as needed -->
            </tr>
            <tr>
                <td>Context Example</td>
                <td>Practical example that shows the term in a context.</td>
                <td>Free text entry of a source of a term from the editorial system SMC</td>
                <!-- Add more rows and data as needed -->
            </tr>
            <tr>
                <td>Term Set</td>
                <td>Grouping of the term in a specific product-specific or thematic set or context.</td>
                <td>Standard<br>
                    ABC-Analysis<br>
                    LOGOMATE<br>
                    INSTORE App<br>
                    COMMERCE Cloud<br>
                    POS<br>
                    RETAIL<br>
                    STATCONTROL Cloud<br>
                    UCP<br>
                    UI/UX<br>
                    General Commerce and Logistics Terminology</td>
                <!-- Add more rows and data as needed -->
            </tr>
            <tr>
                <td>Select terminology set</td>
                <td>The "Select terminology set" drop-down menu allows you to select specific terminology sets in order to filter the terms displayed in the table accordingly.</td>
                <td>Standard<br>
                    ABC-Analysis<br>
                    LOGOMATE<br>
                    INSTORE App<br>
                    COMMERCE Cloud<br>
                    POS<br>
                    RETAIL<br>
                    STATCONTROL Cloud<br>
                    UCP<br>
                    UI/UX<br>
                    General Commerce and Logistics Terminology
                </td>
            </tr>
        </tbody>
    </table>

</div>
<footer>
    <small>Automatically generated list by the tool <a href="https://github.com/W45P85/TBX_to_HTML" target="_blank">TBX to HTML</a>.</small>
</footer>
</body>
</html>
"""
    # HTML in Datei schreiben
    with open(html_file_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

    print(f"Successfully converted to {html_file_path}.")


# Funktion zur Vorschau der ausgewählten Spalten
def preview_columns(file_path, selected_columns):
    tree = ET.parse(file_path)
    root = tree.getroot()

    columns = set()

    for entry in root.findall(".//termEntry"):
        for ntig in entry.findall(".//ntig"):
            for term_note in ntig.findall(".//termNote"):
                column_name = term_note.get("type")
                if column_name == 'normativeAuthorization' or column_name.endswith("|String"):
                    columns.add(column_name)

    # Spalten in gewünschter Reihenfolge anordnen
    ordered_columns = ['Concept ID', 'normativeAuthorization', 'Benennungstyp|String', 'Wortklasse|String', 'Genus|String', 'Language' , 'Definition|String', 'Quelle|String', 'Anmerkung|String', 'Kontextbeispiel|String', 'Termset|String']

    # Filtere die ausgewählten Spalten, die auch in der Reihenfolge vorkommen
    selected_columns = [col for col in ordered_columns if col in columns]

    return selected_columns


# Funktion zum Auswählen und Verarbeiten einer TBX-Datei
def choose_file():
    # Dateiauswahldialog anzeigen
    file_path = filedialog.askopenfilename(filetypes=[("TBX files", "*.tbx")])

    # Spaltenauswahl für die Vorschau
    selected_columns = show_column_selection(file_path)




# Zeigt die ausgewählten Spalten
def show_column_selection(file_path):
    selected_columns = None
    columns = preview_columns(file_path, selected_columns)

    # Ersetze die alten Spaltennamen durch die neuen
    new_column_names = {
        'normativeAuthorization': 'Usage',
        'Benennungstyp|String': 'Term type',
        'Wortklasse|String': 'Word class',
        'Genus|String': 'Gender',
        'Definition|String': 'Definition',
        'Quelle|String': 'Source',
        'Anmerkung|String': 'Additional note',
        'Kontextbeispiel|String': 'Context example',
        'Termset|String': 'Term set'
    }

    # Fenster für Spaltenauswahl erstellen
    root = tk.Tk()
    root.title("Column selection")
    root.geometry("300x400")

    selected_columns = []

    scroll_frame = ScrollableFrame(root)
    scroll_frame.pack(fill="both", expand=True)

    global checkboxes
    checkboxes = []

    # Funktion zum weglassen von Spalten
    def on_checkbox_change(column):
        if column in selected_columns:
            selected_columns.remove(column)
        else:
            selected_columns.append(column)

    # Funktion zum auswählen aller Spalten
    def select_all_columns():
        for checkbox in scroll_frame.scrollable_frame.winfo_children():
            checkbox.select()
            column = checkbox.cget("text")
            if column not in selected_columns:
                selected_columns.append(column)

        print(f"Selected columns: {selected_columns}")

    for column in columns:
        var = tk.IntVar()
        checkbox = tk.Checkbutton(scroll_frame.scrollable_frame, text=new_column_names.get(column, column), variable=var, command=lambda col=column: on_checkbox_change(col))
        checkbox.pack(anchor=tk.W)

    select_all_button = tk.Button(root, text="Select all", command=select_all_columns, bg="#009e8b", fg="white")
    select_all_button.pack(pady=10, side=tk.TOP, fill=tk.X)

    # Funktion zum Schließen des Programms
    def on_continue_click():
        date = datetime.now().date()
        root.destroy()
        file_name = "terminology"
        html_file_path = f"{file_name}_{date}.html"
        convert_tbx_to_html(file_path, html_file_path, selected_columns)


    continue_button = tk.Button(root, text="Next", command=on_continue_click, bg="#009e8b", fg="white")
    continue_button.pack(pady=10, side=tk.TOP, fill=tk.X)

    root.mainloop()

    return selected_columns


# GUI-Fenster erstellen
root = tk.Tk()
#root.iconbitmap("favicon.ico")
root.title("Termfinder by User Assistance")
root.geometry("500x213")

# Schaltfläche um TBX-Datei auszuwählen
choose_button = tk.Button(root, text="Select File", command=choose_file, bg="#009e8b", fg="white", width=20, height=2, anchor="center", font=('times', 16, 'bold', 'italic'))
choose_button.pack(pady=20)

# Button zum Schließen des Programms
close_button = tk.Button(root, text="Close", command=root.destroy, bg="#ff6060", fg="white", width=20, height=2, anchor="center", font=('times', 12, 'bold', 'italic'))
close_button.pack(pady=10)

# Label für Info-Text
info_label = tk.Label(root, text="Programmed by Daniel Rukober", fg="blue", cursor="hand2", font=('Arial', 10, 'italic underline'))
info_label.pack(pady=10, padx=10)
info_label.bind("<Button-1>", open_github)

# Starte die GUI
root.mainloop()