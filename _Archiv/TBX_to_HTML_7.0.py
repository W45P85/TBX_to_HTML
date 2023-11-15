import os
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog

def read_tbx(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    term_dict = {}

    # Iteriere über alle termEntry-Elemente
    for term_entry in root.findall(".//termEntry"):
        # Hole die Concept-ID
        concept_id = term_entry.get("id")

        # Initialisiere eine leere Liste für Term-Informationen
        terms_info = []

        # Iteriere über alle langSet-Elemente
        for lang_set in term_entry.findall(".//langSet"):
            # Hole den Sprachcode
            lang_code = lang_set.get("{http://www.w3.org/XML/1998/namespace}lang")

            # Initialisiere ein Dictionary für Term-Informationen
            term_info = {
                "concept_id": concept_id,
                "lang_code": lang_code,
                "term": "",
                "definition": "",
                "source": "",
                # Füge hier weitere Spalten hinzu, die du ausgeben möchtest
            }

            # Iteriere über alle term-Elemente
            for term in lang_set.findall(".//termGrp/term"):
                term_info["term"] = term.text.strip()

            # Iteriere über alle termNote-Elemente
            for term_note in lang_set.findall(".//termGrp/termNote"):
                note_type = term_note.get("type")
                note_value = term_note.text.strip() if term_note.text else ""
                term_info[note_type] = note_value

            terms_info.append(term_info)

        if concept_id and terms_info:
            term_dict[concept_id] = terms_info

    return term_dict

def convert_tbx_to_html(tbx_file_path, html_file_path):
    tree = ET.parse(tbx_file_path)
    root = tree.getroot()

    file_name = os.path.splitext(os.path.basename(tbx_file_path))[0]

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

        tr.deprecatedTerm {{
            background-color: #ffcccc; /* Hintergrundfarbe für deprecatedTerm */
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
    </style>
</head>
<header>
    <img src="logo.png" alt="Logo Remira">
    <h2>{file_name}</h2>
</header>
<body>

<p>Willkommen zum TBX Viewer! Hier finden Sie eine Liste der Begriffe aus der TBX-Datei.</p>
<p>Verwenden Sie das Suchfeld, um die Tabelle nach Termen zu filtern.</p>

<div class="search-container">
    <input type="text" id="searchInput" placeholder="Suche nach Terme" oninput="updateAutocomplete()">
    <div id="autocomplete" class="autocomplete-items"></div>
</div>
    
<table id="termTable">
    <tr>
        <th>Concept ID</th>
        <th>Term</th>
        <th>Anmerkung</th>
        <th>Benennungstyp</th>
        <th>Definition</th>
        <th>Genus</th>
        <th>Kontextbeispiel</th>
        <th>Numerus</th>
        <th>Quelle</th>
        <th>Termset</th>
        <th>Verwendung</th>
        <th>Wortklasse</th>
        <th>normativeAuthorization</th>
    </tr>
"""

    term_dictionary = read_tbx(tbx_file_path)

    # Populate table rows
    for concept_id, terms_info_list in term_dictionary.items():
        for term_info in terms_info_list:
            html_content += f"<tr>"
            html_content += f"<td>{term_info['concept_id']}</td>"
            html_content += f"<td>{term_info['term']}</td>"

            # Iteriere über vordefinierte Header und füge die entsprechenden Werte hinzu
            for header in [
                "Anmerkung",
                "Benennungstyp",
                "Definition",
                "Genus",
                "Kontextbeispiel",
                "Numerus",
                "Quelle",
                "Termset",
                "Verwendung",
                "Wortklasse",
                "normativeAuthorization"
            ]:
                # Wenn der Header in term_info['notes'] vorhanden ist, nimm den Wert, sonst '-'
                note_value = term_info.get(header, "-")
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
</script>

<footer>
    Programmiert von Daniel Rukober - User Assistance
</footer>
</body>
</html>
"""

    with open(html_file_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

    print(f"Erfolgreich in {html_file_path} konvertiert.")

def choose_file():
    file_path = filedialog.askopenfilename(filetypes=[("TBX files", "*.tbx")])
    if file_path:
        html_file_path = "ausgabe.html"
        convert_tbx_to_html(file_path, html_file_path)

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