import os                               # Betgriebssystem-spezifische Funktionen
import xml.etree.ElementTree as ET      # Verarbeitung von XML-Daten
import tkinter as tk                    # GUI-Bibliothek
from tkinter import filedialog          # Dateidialog-Funktionalität
from datetime import datetime           # Datumsanzeige

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
        self.frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Scrollable Frame
        self.scrollable_frame = tk.Frame(self.frame, background="#ffffff")
        self.scrollable_frame.pack(fill="both", expand=True)

    # Event-Handler: Frame-Größe ändern
    def on_frame_configure(self, event):
            # Canvas an die Größe des Frames anpassen
            canvas_width = event.width

    # Event-Handler: Canvas-Größe ändern
    def on_canvas_configure(self, event):
            # Scrollable Frame an die Größe des Canvas anpassen
            canvas_width = event.width
            self.canvas.itemconfig("self.frame", width=canvas_width)


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

    file_name = os.path.splitext(os.path.basename(file_path))[0]
    date = datetime.now().date()

    # Ersetze die alten Spaltennamen durch die neuen
    new_column_names = {
        'normativeAuthorization': 'Verwendung / Usage',
        'Benennungstyp|String': 'Benennungstyp / Term type',
        'Wortklasse|String': 'Wortklasse / Word class',
        'Genus|String': 'Genus / Gender',
        'Definition|String': 'Definition',
        'Quelle|String': 'Quelle / Source',
        'Anmerkung|String': 'Anmerkung / Additional note',
        'Kontextbeispiel|String': 'Kontextbeispiel / Context example',
        'Termset|String': 'Termset / Term set'
    }

    # HTML-Inhalt erstellen
    html_content = f"""
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/x-icon" href="img\\favicon.ico">
    <title>TBX in HTML konvertiert</title>
    <style>
        body {{
            font-family: Calibri;
            background-color: #f4f4f4;
            margin: 0;
            text-align: center;
            padding: 0;
        }}

        header {{
            text-align: left;
        }}

        img {{
            max-width: 170px;
            padding: 10px;
        }}
        
        h2 {{
            color: #333;
            text-align: center;
            font-size: 40px;
        }}

        .search-container {{
            margin-top: 20px;
        }}

        p {{
            color: #555;
        }}

        input[type="text"] {{
            text-align: center;
            padding: 8px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }}

        button {{
            background-color: #003366;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }}

        button:hover {{
            background-color: #45a049;
        }}
        
        .hidden {{
            display: none;
            }}

        table {{
            border: solid #000000;
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}

        th, td {{
            border: thin solid #000000;
            vertical-align: top;
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}

        footer {{
            text-align: center;
            font-style: italic;
            margin: 20px;
            padding: 20px;
        }}

        th {{
            background-color: #005D6B;
            color: white;
        }}

        tr:hover {{
            background-color: #f5f5f5;
        }}

        .english-table {{
            display: none;
        }}
    </style>
</head>
<header>
    <!-- <img src="img\logo.PNG" alt="Logo Remira"> -->
    <h1>REMIRA terminology</h1>
    <small>{date}</small>
</header>
<body>

<p>Welcome to the terminology database. Here you will find a list of permitted and prohibited terms that should be used depending on the application.</p>
<p>Use the search field to search the table for terms.</p>
<p>In addition to the search function, the table can also be filtered using the drop-down menu.</p>
<p>There is a small legend at the bottom of the page in case you have any initial questions.</p>

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
            <option value="Handelterminologie">Handelsterminologie</option>
            <!-- Bei Bedarf weitere hinzufügen -->
        </select>
    <br />
    <br />
    <!-- Dropdown-Menü zur Auswahl der Sprache -->
        <label for="languageSelect">Select Language</label>
        <select id="languageSelect" onchange="filterTableLanguage()">
            <option value="">All</option>
            <option value="en-us">English</option>
            <option value="de">Deutsch</option>
            <!-- Bei Bedarf weitere hinzufügen -->
</select>
</div>
    
<table id="termTable">
    <tr>
        <th>Concept ID</th>
        <th>Sprache / Language</th>
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

            // Loop durch jede Zeile (überspringe die erste Zeile, die die Überschriften enthält)
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

    function updateSuggestions(filter) {
        var suggestions = [];
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

function filterTable() {
    var selectedLanguage = document.getElementById("languageSelect").value.toUpperCase();
    var selectedFilter = document.getElementById("filterSelect").value.toUpperCase();

    var table = document.getElementById("termTable");
    var rows = table.getElementsByTagName("tr");

    for (var i = 1; i < rows.length; i++) {
        var languageCell = rows[i].getElementsByTagName("td")[1].textContent.toUpperCase();
        var termsetCell = rows[i].getElementsByTagName("td")[11].textContent.toUpperCase();

        var languageFilterPassed = selectedLanguage === "" || languageCell === selectedLanguage;
        var filterFilterPassed = selectedFilter === "ALL" || termsetCell.includes(selectedFilter);

        // Zeige die Zeile, wenn der Sprachfilter oder der Termsetfilter zutrifft
        if (languageFilterPassed && filterFilterPassed) {
            rows[i].classList.remove('hidden');
        } else {
            rows[i].classList.add('hidden');
        }
    }
}










    document.addEventListener("DOMContentLoaded", function () {
        var filterSelect = document.getElementById('filterSelect');
        var languageSelect = document.getElementById('languageSelect');

        filterSelect.addEventListener('change', function () {
            filterTable(); // Filter nach Sprache und Termset
        });

        languageSelect.addEventListener('change', function () {
            filterTable(); // Filter nach Sprache und Termset
        });
    });

    function toggleTable() {
        var germanTable = document.getElementById('german-table');
        var englishTable = document.getElementById('english-table');

        if (document.getElementById('language-toggle').checked) {
            // Englische Tabelle anzeigen, deutsche Tabelle ausblenden
            germanTable.style.display = 'none';
            englishTable.style.display = 'table';
        } else {
            // Deutsche Tabelle anzeigen, englische Tabelle ausblenden
            germanTable.style.display = 'table';
            englishTable.style.display = 'none';
        }
    }
</script>



<h1>Legende</h1>

<label for="language-toggle">English version</label>
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
                <td>Sprache / Language</td>
                <td>Jeweilige Sprache eines Terms innerhalb einer Termgruppe.</td>
                <td>de (Deutsch - Deutschland)<br>en_US (Englisch - USA)</td>
                <!-- Weitere Zeilen und Daten nach Bedarf -->
            </tr>
            <tr>
                <td>Verwendung / Usage</td>
                <td>Jeweilige Verwendungseinstufung eines Terms</td>
                <td>preferredTerm (Bevorzugter Begriff)<br>admittedTerm (Erlaubter Begriff/ Wörterbucheintrag)<br>deprecatedTerm (Gesperrter Begriff)</td>
                <!-- Weitere Zeilen und Daten nach Bedarf -->
            </tr>
            <tr>
                <td>Benennungstyp / Term type</td>
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
                <td>Wortklasse / Word class</td>
                <td>Lexikalische Kategorie eines Terms (z.B. Verb)</td>
                <td>Substantiv: Nomen<br>Verb: Tätigkeitswort<br>Adjektiv: Eigenschaftswort<br>Adverb: Umstandswort</td>
                <!-- Weitere Zeilen und Daten nach Bedarf -->
            </tr>
            <tr>
                <td>Genus / Gender</td>
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
                <td>Quelle / Source</td>
                <td>Ursprung oder Referenz, woher der Term stammt.</td>
                <td>Freitexteingabe einer Quelle eines Terms aus dem Redaktionssystem SMC</td>
                <!-- Weitere Zeilen und Daten nach Bedarf -->
            </tr>
            <tr>
                <td>Anmerkung / Additional note</td>
                <td>Zusätzliche Information für einen Term, insbesondere für Produkte.</td>
                <td>Freitexteingabe einer Quelle eines Terms aus dem Redaktionssystem SMC</td>
                <!-- Weitere Zeilen und Daten nach Bedarf -->
            </tr>
            <tr>
                <td>Kontextbeispiel / Context example</td>
                <td>Praktisches Beispiel, das den Term in einem Kontext zeigt.</td>
                <td>Freitexteingabe einer Quelle eines Terms aus dem Redaktionssystem SMC</td>
                <!-- Weitere Zeilen und Daten nach Bedarf -->
            </tr>
            <tr>
                <td>Termset / Term set</td>
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
                <td>Hauptbenennung: Primary destignation<br>
                    Gemeinschaftliche Benennung: General designation<br>
                    Kurzform: Shorthand designation<br>
                    Abkürzung: Abbreviation<br>
                    Standardtext: Standard Text<br>
                    Synonym: Synonym<br>
                    Variante: Variant
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
                    ABC Analysis<br>
                    LOGOMATE<br>
                    INSTORE App<br>
                    RCC<br>
                    RPOS<br>
                    RETAIL<br>
                    STATCONTROL<br>
                    UCP<br>
                    UI/UX<br>
                    Trade Terminology</td>
                <!-- Add more rows and data as needed -->
            </tr>
            <tr>
                <td>Select terminology set</td>
                <td>The "Select terminology set" drop-down menu allows you to select specific terminology sets in order to filter the terms displayed in the table accordingly.</td>
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

</div>
<footer>
    User Assistance - 2023
</footer>
</body>
</html>
"""
    # HTML in Datei schreiben
    with open(html_file_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

    print(f"Erfolgreich in {html_file_path} konvertiert.")


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

    # Spalten nach deiner gewünschten Reihenfolge anordnen
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
       
    if selected_columns:
        # Rufe die Funktion preview_columns mit beiden Argumenten auf
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        columns = preview_columns(file_path, selected_columns)

        html_file_path = f"{file_name}_in_HTML.html"
        convert_tbx_to_html(file_path, html_file_path, selected_columns)


# Zeigt die ausgewählten Spalten
def show_column_selection(file_path):
    selected_columns = None
    columns = preview_columns(file_path, selected_columns)

    # Ersetze die alten Spaltennamen durch die neuen
    new_column_names = {
        'normativeAuthorization': 'Verwendung / Usage',
        'Benennungstyp|String': 'Benennungstyp / Term type',
        'Wortklasse|String': 'Wortklasse / Word class',
        'Genus|String': 'Genus / Gender',
        'Definition|String': 'Definition',
        'Quelle|String': 'Quelle / Source',
        'Anmerkung|String': 'Anmerkung / Additional note',
        'Kontextbeispiel|String': 'Kontextbeispiel / Context example',
        'Termset|String': 'Termset / Term set'
    }
    
    # Fenster für Spaltenauswahl erstellen
    root = tk.Tk()
    root.title("Spaltenauswahl")
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
        
        print(f"Ausgewählte Spalten: {selected_columns}")

    for column in columns:
        var = tk.IntVar()
        checkbox = tk.Checkbutton(scroll_frame.scrollable_frame, text=new_column_names.get(column, column), variable=var, command=lambda col=column: on_checkbox_change(col))
        checkbox.pack(anchor=tk.W)

    select_all_button = tk.Button(root, text="Alle auswählen", command=select_all_columns, bg="#003366", fg="white")
    select_all_button.pack(pady=10, side=tk.TOP, fill=tk.X)

    # Funktion zum Schließen des Programms
    def on_continue_click():
        root.destroy()
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        html_file_path = f"{file_name}_in_HTML.html"
        convert_tbx_to_html(file_path, html_file_path, selected_columns)


    continue_button = tk.Button(root, text="Weiter", command=on_continue_click, bg="#003366", fg="white")
    continue_button.pack(pady=10, side=tk.TOP, fill=tk.X)

    root.mainloop()

    return selected_columns



# GUI-Fenster erstellen
root = tk.Tk()
root.title("TBX to HTML Converter")
root.geometry("500x150")

# Schaltfläche um TBX-Datei auszuwählen
choose_button = tk.Button(root, text="Datei auswählen", command=choose_file)
choose_button.pack(pady=20)

# Button zum Schließen des Programms
close_button = tk.Button(root, text="Programm schließen", command=root.destroy)
close_button.pack(pady=10)

# Label für Info-Text
info_label = tk.Label(root, text="Programmed by Daniel Rukober - User Assistance", anchor="w", justify="left")
info_label.pack(pady=10, padx=10)

# Starte die GUI
root.mainloop()