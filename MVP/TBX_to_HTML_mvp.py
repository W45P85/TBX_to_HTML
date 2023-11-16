import os
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog

class ScrollableFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw", tags="self.frame")

        self.frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        self.scrollable_frame = tk.Frame(self.frame, background="#ffffff")
        self.scrollable_frame.pack(fill="both", expand=True)

    def on_frame_configure(self, event):
            # Resize the canvas to fit the frame width and height
            canvas_width = event.width

    def on_canvas_configure(self, event):
            # Resize scrollable frame to fit canvas size
            canvas_width = event.width
            self.canvas.itemconfig("self.frame", width=canvas_width)

def read_tbx(file_path, selected_columns):
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

def convert_tbx_to_html(file_path, html_file_path, selected_columns):
    term_dictionary = read_tbx(file_path, selected_columns)

    file_name = os.path.splitext(os.path.basename(file_path))[0]

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

    html_content = f"""
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
            background-color: #003366;
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
    <img src="logo.png" alt="Logo Remira">
    <h2>{file_name}</h2>
</header>
<body>

<p>Willkommen zum TBX Viewer! Hier finden Sie eine Liste der Begriffe aus der TBX-Datei.</p>
<p>Verwenden Sie das Suchfeld, um die Tabelle nach Termen zu filtern.</p>
<p>Am Ende der Tabelle ist eine kleine Legende, falls erste Fragen sind</p>

<div class="search-container">
    <input type="text" id="searchInput" placeholder="Suche nach Terme" oninput="updateAutocomplete()">
    <div id="autocomplete" class="autocomplete-items"></div>
    <!-- <button onclick="highlightTableRows()">Zeige erlaubte Terme</button> -->
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
            var input, filter, table, tr, td, i, j, txtValue, found;
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

                // Wenn die Sucheingabe nicht leer ist, filtere die Zeilen
                if (filter.trim() !== '') {
                    td = tr[i].getElementsByTagName('td');
                    found = false;

                    // Überprüfe jede Zelle in der Zeile
                    for (j = 0; j < td.length; j++) {
                        txtValue = td[j].textContent || td[j].innerText;
                        if (txtValue.toUpperCase().indexOf(filter) > -1) {
                            found = true;

                            // Extrahiere die Concept-ID der gefundenen Zeile
                            var conceptId = tr[i].getElementsByTagName('td')[0].textContent || tr[i].getElementsByTagName('td')[0].innerText;

                            // Speichere die Concept-ID, wenn sie noch nicht gespeichert wurde
                            if (!visibleConceptIds.includes(conceptId)) {
                                visibleConceptIds.push(conceptId);
                            }

                            break;
                        }
                    }

                    // Wenn keine der Zellen den Filter enthält, verstecke die Zeile
                    if (!found) {
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

<h2>Legende</h2>

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
                <td>Maskulinum: Männlich<br>Femininum: Weiblich<br>Neutrum: Sächlich</td>
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
        </tbody>
    </table>

    <table id="english-table" class="english-table">
        <!-- Englische Tabelle (initial ausgeblendet) -->
        <thead>
            <tr>
                <th>Column name</th>
                <th>Description</th>
                <th>Possible values</th>
                <!-- Add more rows and data as needed -->
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Concept ID</td>
                <td>Unique identification number of a term group in the SMC editing system. Different terms can belong to one term group</td>.
                <td>In ascending numbering (e.g. concept-xxx)</td>
                <!-- Further lines and data as required -->
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

    with open(html_file_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

    print(f"Erfolgreich in {html_file_path} konvertiert.")


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

    # Hier kannst du die Spalten nach deiner gewünschten Reihenfolge anordnen
    ordered_columns = ['Concept ID', 'normativeAuthorization', 'Benennungstyp|String', 'Wortklasse|String', 'Genus|String', 'Language' , 'Definition|String', 'Quelle|String', 'Anmerkung|String', 'Kontextbeispiel|String', 'Termset|String']

    # Filtere nur die ausgewählten Spalten, die auch in der Reihenfolge vorkommen
    selected_columns = [col for col in ordered_columns if col in columns]

    return selected_columns


def choose_file():
    # Get the file path
    file_path = filedialog.askopenfilename(filetypes=[("TBX files", "*.tbx")])

    # Get the selected columns
    selected_columns = show_column_selection(file_path)
       
    if selected_columns:
        # Call the preview_columns function with both arguments
        columns = preview_columns(file_path, selected_columns)

        html_file_path = "ausgabe.html"
        convert_tbx_to_html(file_path, html_file_path, selected_columns)


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
    
    root = tk.Tk()
    root.title("Spaltenauswahl")
    root.geometry("300x400")

    selected_columns = []

    scroll_frame = ScrollableFrame(root)
    scroll_frame.pack(fill="both", expand=True)

    global checkboxes
    checkboxes = []

    # Funktion hier definieren
    def on_checkbox_change(column):
        if column in selected_columns:
            selected_columns.remove(column)
        else:
            selected_columns.append(column)

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

    def on_continue_click():
        root.destroy()
        html_file_path = "ausgabe.html"
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