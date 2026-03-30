#!/usr/bin/python3
import os                                           # Betgriebssystem-spezifische Funktionen
import xml.etree.ElementTree as ET                  # Verarbeitung von XML-Daten
import tkinter as tk                                # GUI-Bibliothek
from tkinter import filedialog                      # Dateidialog-Funktionalität
from datetime import datetime                       # Datumsanzeige
import webbrowser
from tkinter import *
from tkinter.ttk import *                           # Für Links in tkInter benötigt

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
        display: none;
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
    }}

    .tooltip:hover .tooltiptext {{
        display: block;
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
        margin: 0px;
        font-size: 2rem;
        padding-left: 10px;
    }}
    
    h1_legende {{
        font-weight: 600;
        font-size: 2rem;
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
        position: sticky;
        top: 0;
        z-index: 100;
    }}

    tr:nth-child(even) {{
        background-color: #f2f2f2;
    }}
    
    .pagination {{
        margin: 20px 0;
        text-align: center;
    }}
    
    .pagination button {{
        margin: 0 5px;
        padding: 8px 16px;
    }}
    
    .pagination button.active {{
        background-color: #009e8b;
    }}
    
    .pagination button:disabled {{
        background-color: #ccc;
        cursor: not-allowed;
    }}
    
    #pageInfo {{
        margin: 10px 0;
        font-weight: bold;
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
    
    .preferred-term {{
            background-color: lightgreen;
            color: darkgreen;
        }}
        
        .deprecated-term {{
            background-color: lightcoral;
            color: darkred;
        }}
        
        .admitted-term {{
            background-color: lightgray;
            color: black;
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
    <input type="text" id="searchInput" placeholder="Search for terms">
    <div id="autocomplete" class="autocomplete-items"></div>
    <br />
    <br />
    <!-- Dropdown-Menü zur Auswahl der Sprache -->
        <label for="languageSelect">Select Language</label>
        <select id="languageSelect" onchange="filterTable()">
            <option value="" selected>All</option>
            <option value="en-us">English</option>
            <option value="de">Deutsch</option>
            <!-- Bei Bedarf weitere hinzufügen -->
        </select>
</div>

<div id="pageInfo"></div>
<div class="pagination" id="paginationTop"></div>

<table id="termTable">
    <tr>
        <th>Concept ID</th>
        <th>Language</th>
        <th>Term</th>
        <!-- Add headers here -->
"""

    # PERFORMANCE FIX: Use list instead of string concatenation
    html_parts = []
    
    for column in selected_columns:
        html_parts.append(f"<th>{column}</th>\n")

    html_parts.append("</tr>\n")

    # Build table rows efficiently
    for concept_id, terms_info in term_dictionary.items():
        for term_info in terms_info:
            html_parts.append(f"<tr>")
            html_parts.append(f"<td>{concept_id}</td>")
            html_parts.append(f"<td>{term_info['language']}</td>")
            html_parts.append(f"<td>{term_info['term']}</td>")

            for column in selected_columns:
                # Verwende den ursprünglichen Spaltennamen für die Zuordnung des Inhalts
                original_column_name = next((key for key, value in new_column_names.items() if value == column), column)
                note_value = term_info["notes"].get(original_column_name, "-")
                html_parts.append(f"<td>{note_value}</td>")

            html_parts.append("</tr>\n")

    html_parts.append("</table>\n")
    html_parts.append('<div class="pagination" id="paginationBottom"></div>\n')
    
    # Join all parts at once (much faster!)
    html_content += ''.join(html_parts)
    html_content += """

<script>
// ============================================
// PERFORMANCE OPTIMIZED VERSION
// ============================================

// Global state
var currentPage = 1;
var rowsPerPage = 50; // PERFORMANCE: Reduced from 100 to 50
var allRows = [];
var filteredRows = [];
var searchTimeout;

window.onload = function() {
    console.time('Page Load Performance');
    initializeTableOptimized();
    filterTable();
    toggleTable();
    console.timeEnd('Page Load Performance');
};

/**
 * AGGRESSIVE PERFORMANCE FIX: Minimal initialization - lazy load everything else
 */
function initializeTableOptimized() {
    var table = document.getElementById("termTable");
    if (!table) return;
    
    var rows = table.getElementsByTagName('tr');
    
    // Store all rows - NO processing yet!
    allRows = Array.from(rows).slice(1); // Skip header
    filteredRows = allRows.slice();
    
    // ONLY colorize Usage column (column 3) - this is fast
    for (var i = 0; i < allRows.length; i++) {
        var cells = allRows[i].getElementsByTagName('td');
        if (cells.length > 3) {
            var usageCell = cells[3];
            var cellText = usageCell.innerText.trim();
            
            if (cellText === 'preferredTerm') {
                usageCell.classList.add('preferred-term');
            } else if (cellText === 'deprecatedTerm') {
                usageCell.classList.add('deprecated-term');
            } else if (cellText === 'admittedTerm') {
                usageCell.classList.add('admitted-term');
            }
        }
    }
    
    // Initialize pagination
    displayPage(1);
    
    // Add search event with debouncing
    document.getElementById('searchInput').addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(function() {
            updateAutocomplete();
        }, 300);
    });
    
    // LAZY LOAD: Process tooltips and links only for visible rows
    setTimeout(function() {
        processVisibleRowsLazy();
    }, 100);
}

/**
 * LAZY LOAD: Only process currently visible rows
 */
function processVisibleRowsLazy() {
    var tooltipMap = createTooltipMap();
    
    for (var i = 0; i < allRows.length; i++) {
        var row = allRows[i];
        
        // Only process if visible
        if (!row.classList.contains('hidden')) {
            var cells = row.getElementsByTagName('td');
            
            for (var j = 0; j < cells.length; j++) {
                var cell = cells[j];
                
                // Skip if already processed
                if (cell.dataset.processed) continue;
                
                var cellText = cell.innerText.trim();
                var cellHTML = cell.innerHTML;
                
                // Add tooltips
                if (tooltipMap[cellText] && !cell.classList.contains('tooltip')) {
                    cell.classList.add("tooltip");
                    cell.innerHTML += '<span class="tooltiptext">' + tooltipMap[cellText] + '</span>';
                }
                
                // Convert URLs to links
                if ((cellHTML.includes('http://') || cellHTML.includes('https://')) && !cell.querySelector('a')) {
                    convertCellUrlToLink(cell);
                }
                
                cell.dataset.processed = 'true';
            }
        }
    }
}

/**
 * Create tooltip lookup map for O(1) access
 */
function createTooltipMap() {
    var tooltips = [
        ["Hauptbenennung", "This is the main term designation."],
        ["Substantiv", "This is a noun."],
        ["Verb", "This is a verb."],
        ["Adjektiv", "This is an adjective."],
        ["Adverb", "This is an adverb."],
        ["Synonym", "This is a synonym term."],
        ["Gemeinsprachlich", "This is a common language term"],
        ["Variante", "This is a variant term."],
        ["Abkürzung", "This is a term abbreviation."],
        ["Kurzform", "This is a short-form term."],
        ["Standardtext", "This is standard usage term."],
        ["Femininum", "This is feminine."],
        ["Masculinum", "This is masculine."],
        ["Neutrum", "This is neuter."],
        ["Handelterminologie", "This is the General Commerce and Logistics Terminology."]
    ];
    
    var map = {};
    for (var i = 0; i < tooltips.length; i++) {
        map[tooltips[i][0]] = tooltips[i][1];
    }
    return map;
}

/**
 * Helper function to convert URL in cell to clickable link
 */
function convertCellUrlToLink(cell) {
    var cellContent = cell.innerHTML;
    var urlRegex = /(https?:\/\/[^\s]+)/g;
    var matches = cellContent.match(urlRegex);
    
    if (matches && !cellContent.includes("(translation)")) {
        var link = document.createElement("a");
        link.href = matches[0];
        link.textContent = matches[0];
        link.target = "_blank";
        
        var textBefore = cellContent.substring(0, cellContent.indexOf(matches[0]));
        var remainingText = cellContent.substring(cellContent.indexOf(matches[0]) + matches[0].length);
        
        cell.innerHTML = '';
        if (textBefore) {
            cell.appendChild(document.createTextNode(textBefore));
        }
        cell.appendChild(link);
        cell.appendChild(document.createTextNode(remainingText));
    } else if (cellContent.includes("(translation)")) {
        var parts = cellContent.split("(translation)");
        var linkBefore = document.createElement("a");
        linkBefore.href = parts[0].trim();
        linkBefore.textContent = parts[0].trim();
        linkBefore.target = "_blank";
        
        cell.innerHTML = '';
        cell.appendChild(linkBefore);
        cell.appendChild(document.createTextNode("(translation)" + parts[1]));
    }
}



/**
 * PERFORMANCE: Optimized search with pagination support
 */
function updateAutocomplete() {
    var input = document.getElementById('searchInput');
    var filter = input.value.toUpperCase();

    if (filter.trim() === '') {
        filteredRows = allRows.slice();
        currentPage = 1;
        displayPage(1);
        return;
    }

    // Array to store visible concept IDs
    var visibleConceptIds = new Set();

    // Search in Term column (index 2)
    for (var i = 0; i < allRows.length; i++) {
        var td = allRows[i].getElementsByTagName('td')[2];
        if (td) {
            var txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                var conceptId = allRows[i].getElementsByTagName('td')[0].textContent;
                visibleConceptIds.add(conceptId);
            }
        }
    }

    // Filter rows by concept ID
    filteredRows = allRows.filter(function(row) {
        var conceptId = row.getElementsByTagName('td')[0].textContent;
        return visibleConceptIds.has(conceptId);
    });

    currentPage = 1;
    displayPage(1);
    updateSuggestions(filter);
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



/**
 * PERFORMANCE: Optimized language filter with pagination
 */
function filterTable() {
    var selectedLanguage = document.getElementById("languageSelect").value.toUpperCase();
    var searchFilter = document.getElementById('searchInput').value.toUpperCase();

    // Filter by language
    if (selectedLanguage === "") {
        filteredRows = allRows.slice();
    } else {
        filteredRows = allRows.filter(function(row) {
            var languageCell = row.getElementsByTagName("td")[1].textContent.toUpperCase();
            return languageCell === selectedLanguage;
        });
    }

    // Apply search filter if exists
    if (searchFilter.trim() !== '') {
        var visibleConceptIds = new Set();
        
        for (var i = 0; i < filteredRows.length; i++) {
            var td = filteredRows[i].getElementsByTagName('td')[2];
            if (td) {
                var txtValue = td.textContent || td.innerText;
                if (txtValue.toUpperCase().indexOf(searchFilter) > -1) {
                    var conceptId = filteredRows[i].getElementsByTagName('td')[0].textContent;
                    visibleConceptIds.add(conceptId);
                }
            }
        }
        
        filteredRows = filteredRows.filter(function(row) {
            var conceptId = row.getElementsByTagName('td')[0].textContent;
            return visibleConceptIds.has(conceptId);
        });
    }

    currentPage = 1;
    displayPage(1);
}

/**
 * Display specific page with pagination
 */
function displayPage(pageNum) {
    currentPage = pageNum;
    
    // Hide all rows first
    for (var i = 0; i < allRows.length; i++) {
        allRows[i].classList.add('hidden');
    }
    
    // Calculate pagination
    var startIndex = (pageNum - 1) * rowsPerPage;
    var endIndex = Math.min(startIndex + rowsPerPage, filteredRows.length);
    
    // Show only current page rows
    for (var i = startIndex; i < endIndex; i++) {
        filteredRows[i].classList.remove('hidden');
    }
    
    // Update pagination controls
    updatePaginationControls();
    
    // LAZY LOAD: Process newly visible rows after a short delay
    setTimeout(function() {
        processVisibleRowsLazy();
    }, 50);
}

/**
 * Create/Update pagination controls
 */
function updatePaginationControls() {
    var totalPages = Math.ceil(filteredRows.length / rowsPerPage);
    
    var pageInfo = 'Showing ' + 
        ((currentPage - 1) * rowsPerPage + 1) + '-' + 
        Math.min(currentPage * rowsPerPage, filteredRows.length) + 
        ' of ' + filteredRows.length + ' entries';
    
    document.getElementById('pageInfo').textContent = pageInfo;
    
    var paginationHTML = '';
    
    // Previous button
    paginationHTML += '<button onclick="displayPage(' + (currentPage - 1) + ')" ' + 
        (currentPage === 1 ? 'disabled' : '') + '>← Previous</button>';
    
    // Page numbers (show max 5 pages)
    var startPage = Math.max(1, currentPage - 2);
    var endPage = Math.min(totalPages, currentPage + 2);
    
    if (startPage > 1) {
        paginationHTML += '<button onclick="displayPage(1)">1</button>';
        if (startPage > 2) paginationHTML += '<span>...</span>';
    }
    
    for (var i = startPage; i <= endPage; i++) {
        paginationHTML += '<button onclick="displayPage(' + i + ')" ' + 
            (i === currentPage ? 'class="active"' : '') + '>' + i + '</button>';
    }
    
    if (endPage < totalPages) {
        if (endPage < totalPages - 1) paginationHTML += '<span>...</span>';
        paginationHTML += '<button onclick="displayPage(' + totalPages + ')">' + totalPages + '</button>';
    }
    
    // Next button
    paginationHTML += '<button onclick="displayPage(' + (currentPage + 1) + ')" ' + 
        (currentPage === totalPages ? 'disabled' : '') + '>Next →</button>';
    
    document.getElementById('paginationTop').innerHTML = paginationHTML;
    document.getElementById('paginationBottom').innerHTML = paginationHTML;
}


// Function to add event listeners for filter and language selection
document.addEventListener("DOMContentLoaded", function () {
    var filterSelect = document.getElementById('filterSelect');
    var languageSelect = document.getElementById('languageSelect');

    // Add event listener for filter selection change
    filterSelect.addEventListener('change', function () {
        filterTable();
    });

    // Add event listener for language selection change
    languageSelect.addEventListener('change', function () {
        filterTable();
    });
});


/**
* Function to toggle between German and English legend.
* Shows the corresponding table based on the toggle checkbox state.
*/
function toggleTable() {
    var germanTable = document.getElementById('german-table');
    var englishTable = document.getElementById('english-table');

    // Check if the language toggle checkbox is checked
    if (document.getElementById('language-toggle').checked) {
        germanTable.style.display = 'table';
        englishTable.style.display = 'none';
    } else {
        germanTable.style.display = 'none';
        englishTable.style.display = 'table';
    }
}

// OLD FUNCTIONS REMOVED - Now handled by initializeTableOptimized()
// - addTooltipsFromTable() 
// - convertUrlsToLinks()
// - colorizeTerms()
// These are now combined in a single loop for better performance

</script>
<br>
<br>
<br>
<h1_legende id="legend">Legend</h1_legende>
<br>
<br>

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
        </tbody>
    </table>

</div>
<footer>
    <small>This list was created automatically by the tool <a href="https://github.com/W45P85/TBX_to_HTML" target="_blank">TBX to HTML</a>.</small>
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
    ordered_columns = ['Concept ID', 'normativeAuthorization', 'Benennungstyp|String', 'Wortklasse|String', 'Genus|String', 'Language' , 'Definition|String', 'Quelle|String', 'Anmerkung|String', 'Kontextbeispiel|String']

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
    }

    # Fenster für Spaltenauswahl erstellen
    root = tk.Tk()
    root.title("Column selection")
    root.geometry("300x360")

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

    select_all_button = tk.Button(root, text="Select all", command=select_all_columns, bg="#009e8b", fg="white", height=1, anchor="center")
    select_all_button.pack(pady=10, side=tk.TOP, fill=tk.X)

    # Funktion zum Schließen des Programms
    def on_continue_click():
        date = datetime.now().date()
        root.destroy()
        file_name = "terminology"
        html_file_path = f"{file_name}_{date}.html"
        convert_tbx_to_html(file_path, html_file_path, selected_columns)


    continue_button = tk.Button(root, text="Next", command=on_continue_click, bg="#585858", fg="white", height=1, anchor="center")
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