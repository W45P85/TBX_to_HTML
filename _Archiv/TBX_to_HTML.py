import os
import xml.etree.ElementTree as ET
from jinja2 import Environment, FileSystemLoader
from tkinter import Tk, filedialog

# Hilfsfunktion zum Extrahieren von Werten aus <termNote> Tags
def get_term_note_value(termEntry, note_type):
    namespace = {"tb": "http://www.w3.org/XML/1998/namespace"}
    note_element = termEntry.find(f".//tb:termNote[@type='{note_type}']", namespaces=namespace)
    return note_element.text if note_element is not None else ""


# Funktion zum Extrahieren der Daten aus der TBX-Datei
def extract_tbx_data(tbx_file):
    tree = ET.parse(tbx_file)
    root = tree.getroot()

    data = []
    namespaces = {"tb": "http://www.tei-c.org/ns/1.0", "xml": "http://www.w3.org/XML/1998/namespace"}
    for termEntry in root.findall(".//tb:termEntry", namespaces=namespaces):
        concept_id = termEntry.attrib.get("id")

        # Überprüfen, ob das <Term> Tag vorhanden ist
        term_element = termEntry.find(".//tb:term", namespaces=namespaces)
        term = term_element.text if term_element is not None else ""

        language_element = termEntry.find(".//tb:langSet[@xml:lang='de']", namespaces=namespaces)
        language = language_element.text if language_element is not None else ""

        entry_data = {
            "Concept ID": concept_id,
            "Term": term,
            "Verwendung / Usage": get_term_note_value(termEntry, "normativeAuthorization"),
            "Benennungstyp / Term type": get_term_note_value(termEntry, "Benennungstyp|String"),
            "Wortart / Word class": get_term_note_value(termEntry, "Wortklasse|String"),
            "Genus / Gender": get_term_note_value(termEntry, "Genus|String"),
            "Sprache / Language": get_term_note_value(termEntry, "langSet|de"),
            "Definition": get_term_note_value(termEntry, "Definition|String"),
            "Quelle / Source": get_term_note_value(termEntry, "Quelle|String"),
            "Anmerkung / Additional notes": get_term_note_value(termEntry, "Anmerkung|String"),
            "Kontextbeispiel / Context example": get_term_note_value(termEntry, "Kontextbeispiel|String"),
            "Termset / Term set": get_term_note_value(termEntry, "Termset|String"),
        }

        print("Entry data:", entry_data)
        data.append(entry_data)

    print("Extracted data:", data)
    return data

# Funktion zum Erstellen der HTML-Datei
def create_html(data):
    env = Environment(loader=FileSystemLoader(os.path.dirname(os.path.abspath(__file__))))
    template = env.get_template('template.html')

    html_output = template.render(data=data)

    with open('output.html', 'w', encoding='utf-8') as f:
        f.write(html_output)

# Funktion zum Auswahl der TBX-Datei über den Datei-Dialog
def choose_tbx_file():
    root = Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(
        title="Select TBX File",
        filetypes=[("TBX files", "*.tbx"), ("All files", "*.*")]
    )

    return file_path

# Beispielaufruf
tbx_file_path = choose_tbx_file()

if tbx_file_path:
    tbx_data = extract_tbx_data(tbx_file_path)
    create_html(tbx_data)
    print(f"HTML file generated successfully: output.html")
else:
    print("No TBX file selected.")

input("Drücken Sie Enter zum Beenden...")
