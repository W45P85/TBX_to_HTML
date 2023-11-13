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
    # Define the order of termNote tags
    note_order = ["Definition", "normativeAuthorization", "Quelle", "Anmerkung", "Beispiel", "Genus", "Benennungstyp", "Wortklasse", "Numerus", "Verwendung", "softhyphens", "casesensitive", "Termset"]  # Add or modify as needed

    # Extract relevant information from TBX
    tree = ET.parse(tbx_path)
    root = tree.getroot()

    html_content = f"""<html>
                        <head>
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
                                <h2>{os.path.basename(tbx_path)}</h2>
                            </header>
                            <div id="search_container">
                                <label for='search_term'>Suche Term: </label>
                                <input type='text' placeholder='Term..' id='search_term' onkeyup='searchTerm()'><br><br>
                                <table border='1' id='term_table'>
                                    <tr><th>Term</th>"""

    # Add column headers for each term note type in the specified order
    for note_type in note_order:
        html_content += f"<th>{note_type}</th>"
    html_content += "</tr>"

    term_data_list = []

    for term_entry in root.findall(".//termEntry"):
        term, term_notes = extract_term_data(term_entry, note_order)
        html_content += f"<tr><td>{term}</td>"

        # Add term note values for each corresponding note type
        for note_type in note_order:
            note_value = term_notes.get(note_type, "")
            html_content += f"<td>{note_value}</td>"

        html_content += "</tr>"

    # Sort term data by term
    term_data_list.sort(key=lambda x: x[0])

    # Create a dictionary to store relationships between blocked and allowed terms
    term_relations = {}

    for term_entry in root.findall(".//termEntry"):
        term, term_notes = extract_term_data(term_entry, note_order)
        term_data_list.append((term, term_notes))

    for term, term_notes in term_data_list:
        # Spalte "Term" zuerst einfügen
        html_content += f"<tr><td>{term}</td>"

        # Überprüfe, ob der Begriff deprecated (gesperrt) ist
        is_blocked = "deprecatedTerm" in term_notes.get("normativeAuthorization", "").lower()

        # Wenn der Begriff gesperrt ist, finde den entsprechenden erlaubten Begriff
        if is_blocked:
            allowed_term_id = term_relations.get(term_id, "")
            if allowed_term_id:
                allowed_term_entry = root.find(f".//termEntry[@id='{allowed_term_id}']")
                allowed_term, _ = extract_term_data(allowed_term_entry, note_order)[0]
                html_content += f"<td><a href='#{allowed_term_id}'>{allowed_term}</a></td>"
        else:
            html_content += "<td></td>"

        # Add term note values for each corresponding note type
        for note_type in note_order:
            note_value = term_notes.get(note_type, "")
            html_content += f"<td>{note_value}</td>"

        html_content += "</tr>"

        # If the term is allowed, update the dictionary with the relationship
        if not is_blocked and "concept-" in term_notes.get("normativeAuthorization", ""):
            allowed_term_id = term_notes["normativeAuthorization"].split("concept-")[1].split("|")[0]
            term_relations[term_id] = allowed_term_id

    html_content += "</table>"
    # html_content += "<button onclick='closeProgram()'>Programm schließen</button>"
    html_content += "<p>Programmiert von Daniel Rukober - User Assistance</p>"
    html_content += "<script>"
    html_content += "function searchTerm() {"
    html_content += "var input, filter, table, tr, td, i, txtValue;"
    html_content += "input = document.getElementById('search_term');"
    html_content += "filter = input.value.toUpperCase();"
    html_content += "table = document.getElementById('term_table');"
    html_content += "tr = table.getElementsByTagName('tr');"
    html_content += "for (i = 0; i < tr.length; i++) {"
    html_content += "td = tr[i].getElementsByTagName('td')[0];"
    html_content += "if (td) {txtValue = td.textContent || td.innerText;"
    html_content += "if (txtValue.toUpperCase().indexOf(filter) > -1) {tr[i].style.display = '';}"
    html_content += "else {tr[i].style.display = 'none';}}}};"
    html_content += "function closeProgram() { window.close(); }"
    html_content += "</script></body></html>"

    # Write HTML content to file
    with open(html_file, "w", encoding="utf-8") as html_output:
        html_output.write(html_content)

    return term_relations

def choose_file():
    file_path = filedialog.askopenfilename(filetypes=[("TBX files", "*.tbx")])
    if file_path:
        output_html = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
        term_relations = convert_tbx_to_html(file_path, output_html)
        print("Term Relations:", term_relations)

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
