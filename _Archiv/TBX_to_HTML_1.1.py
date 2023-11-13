import os
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog

def extract_term_data(term_entry, note_order):
    term = term_entry.find(".//term").text
    term_notes = {note.attrib['type'].split('|')[0]: note.text for note in term_entry.findall(".//termNote") if note.text is not None}
    ordered_notes = {note_type: term_notes.get(note_type, "") for note_type in note_order}
    return term, ordered_notes

def convert_tbx_to_html(tbx_path, html_file):
    # Die Sortierfolge der termNote-Tags festlegen
    note_order = ["Definition", "normativeAuthorization", "Quelle", "Anmerkung", "Beispiel", "Genus", "Benennungstyp", "Wortklasse", "Numerus", "Verwendung", "softhyphens", "casesensitive", "Termset"]  # Nach Bedarf hinzufügen oder ändern

    # Extrahieren relevanter Informationen aus TBX
    tree = ET.parse(tbx_path)
    root = tree.getroot()

    # Extrahieren und alphabetisch sortieren
    term_data_list = [extract_term_data(term_entry, note_order) for term_entry in root.findall(".//termEntry")]
    term_data_list.sort(key=lambda x: x[0])  # Sortieren nach Term

    # HTML-Inhalt mit Tabelle und Sucheingabe erstellen
    html_content = f"""
    <html>
    <head>
        <title>TBX to HTML</title>
        <style>
            body {{
                font-family: Calibri;
            }}
            table {{
                border-collapse: collapse;
                width: 80%;
                margin: 20px;
            }}
            .logo {{
                max-width: 170px;
            }}
            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                font-size: 20px;
                background-color: #f2f2f2;
            }}
            td {{
                vertical-align: top;
            }}
            input {{
                padding: 8px;
                margin: 10px;
            }}
            h2 {{
                text-align: center;
                font-size: 40px;
            }}
            footer {{
                text-align: center;
            }}
            .search_term {{
                text-align: center;
                font-size: 15px;
            }}
            #search_container {{
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <header>
            <img src="logo.png" alt="logo" class="logo">
        </header>

        <h2>{os.path.basename(tbx_path)}</h2>
        <div id="search_container"
            <label for='search_term'>Suche Term: </label>
            <input type='text' placeholder='Term..' id='search_term' onkeyup='searchTerm()'><br><br>
            <table border='1' id='term_table'>
                <tr><th>Term</th>
        </div>
    """

    # Spaltenüberschriften in der angegebenen Reihenfolge hinzufügen
    for note_type in note_order:
        html_content += f"<th>{note_type}</th>"

    html_content += "</tr>"

    for term, term_notes in term_data_list:
        html_content += f"<tr><td>{term}</td>"

        # Hinzufügen von Werten für jeden entsprechenden Term
        for note_type in note_order:
            note_value = term_notes.get(note_type, "")
            html_content += f"<td>{note_value}</td>"

        html_content += "</tr>"

    html_content += """
        </table>
        <script>
            function searchTerm() {
                var input, filter, table, tr, td, i, txtValue;
                input = document.getElementById('search_term');
                filter = input.value.toUpperCase();
                table = document.getElementById('term_table');
                tr = table.getElementsByTagName('tr');
                for (i = 0; i < tr.length; i++) {
                    td = tr[i].getElementsByTagName('td')[0];
                    if (td) {
                        txtValue = td.textContent || td.innerText;
                        if (txtValue.toUpperCase().indexOf(filter) > -1) {
                            tr[i].style.display = '';
                        } else {
                            tr[i].style.display = 'none';
                        }
                    }
                }
            };
        </script>
    </body>
    <footer>
        <p>&copy; Daniel Rukober, Commerce Cloud</p>
    </footer>
    </html>
    """

    # HTML-Inhalt in eine Datei schreiben
    with open(html_file, "w", encoding="utf-8") as html_output:
        html_output.write(html_content)

def choose_file():
    file_path = filedialog.askopenfilename(filetypes=[("TBX files", "*.tbx")])
    if file_path:
        output_html = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
        convert_tbx_to_html(file_path, output_html)

# Funktion zum Schließen des Programms
def close_program():
    root.destroy()

# GUI-Fenster erstellen
root = tk.Tk()
root.title("TBX to HTML Converter by Daniel Rukober")
root.geometry("500x150")

# Schaltfläche um TBX-Datei auszuwählen
choose_button = tk.Button(root, text="TBX-Datei auswählen", command=choose_file)
choose_button.pack(pady=20)

# Button zum Schließen des Programms
close_button = tk.Button(root, text="Programm Schließen", command=close_program)
close_button.pack(pady=10)

# Label für Info-Text
info_label = tk.Label(root, text="Programmiert von Daniel Rukober - User Assistance", anchor="w", justify="left")
info_label.pack(pady=10, padx=10)

# Starte die GUI
root.mainloop()
