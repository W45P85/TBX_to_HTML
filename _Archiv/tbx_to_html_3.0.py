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

    # Extract terms and notes, then sort alphabetically by term
    term_data_list = [extract_term_data(term_entry, note_order) for term_entry in root.findall(".//termEntry")]
    term_data_list.sort(key=lambda x: x[0])  # Sort by term

    # Create HTML content with a table and search input
    html_content = f"<html><body><h2>{os.path.basename(tbx_path)}</h2>"
    html_content += "<label for='search_term'>Search Term:</label>"
    html_content += "<input type='text' id='search_term' onkeyup='searchTerm()'><br><br>"
    html_content += "<table border='1' id='term_table'><tr><th>Term</th>"

    # Add column headers for each term note type in the specified order
    for note_type in note_order:
        html_content += f"<th>{note_type}</th>"

    html_content += "</tr>"

    for term, term_notes in term_data_list:
        html_content += f"<tr><td>{term}</td>"

        # Add term note values for each corresponding note type
        for note_type in note_order:
            note_value = term_notes.get(note_type, "")
            html_content += f"<td>{note_value}</td>"

        html_content += "</tr>"

    html_content += "</table><script>"
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
    html_content += "</script></body></html>"

    # Write HTML content to file
    with open(html_file, "w", encoding="utf-8") as html_output:
        html_output.write(html_content)

def choose_file():
    file_path = filedialog.askopenfilename(filetypes=[("TBX files", "*.tbx")])
    if file_path:
        output_html = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
        convert_tbx_to_html(file_path, output_html)

# Create a simple GUI window
root = tk.Tk()
root.title("TBX to HTML Converter")

# Create a button to choose the TBX file
choose_button = tk.Button(root, text="Choose TBX File", command=choose_file)
choose_button.pack(pady=10)

# Start the GUI event loop
root.mainloop()
