<pre style="background-color: transparent; border: none;">

  _____  ____ __  __  _           _   _  _____  __  __  _     
 |_   _|| __ )\ \/ / | |_  ___   | | | ||_   _||  \/  || |    
   | |  |  _ \ \  /  | __|/ _ \  | |_| |  | |  | |\/| || |    
   | |  | |_) |/  \  | |_| (_) | |  _  |  | |  | |  | || |___ 
   |_|  |____//_/\_\  \__|\___/  |_| |_|  |_|  |_|  |_||_____|
                                                              
  
<p>Converter for TBX-files to HTML</p>
</pre>

## Overview
**TBX to HTML** converts TBX files into readable HTML files. It analyzes the TBX file and allows you to select the desired columns for conversion.


## Installation
No installation is required. Simply use the **tbx_to_html.exe** file from the "MVP" folder to start the tool.


## Usage
1. open the program:
       Open the "TBX to HTML" program.
2. select a TBX file:

<img src="MVP/img/Programm%20öffnet%20sich.PNG">

- Click on the "Select file" button.
- Select the desired TBX file from your file system and confirm the selection with "Open".

3. column selection:

<img src="MVP/img/alle_auswählen.PNG" width="250">

- After selecting the file, a window opens to select the columns to be displayed in the HTML document.
- You can select the columns by activating the corresponding checkboxes.
- Alternatively, you can also use the "Select all" option to select all available columns at once (recommended).
- Click on "Next" to continue.

4. conversion:

<img src="MVP/img/Dateiname%20der%20HTML.PNG">


- After the column selection, the TBX file is converted into an HTML document.
- After successful conversion, the HTML is saved in the same directory as the original TBX file. The file is called "terminology_YYYY-MM-DD", whereby the current day is taken as the date.

5. close the program:
       Once the conversion is complete, you can close the program by clicking on red the "Close" button.


## How This Tool Works
This tool  is a Python program that facilitates the conversion of a TBX (TermBase eXchange) file to an HTML format. The program also includes features for previewing and selecting specific columns from the TBX file. The code is divided into two parts, each responsible for different functionalities. Here is a detailed explanation of how the script works:


### Part 1: GUI Setup and TBX File Processing
#### Importing Libraries

```
   import tkinter as tk
   from tkinter import filedialog
   import xml.etree.ElementTree as ET
   from datetime import datetime
```
The script imports necessary libraries for GUI creation (tkinter), file handling (filedialog), XML parsing (ElementTree), and date/time operations (datetime).

#### ScrollableFrame Class

```
   import tkinter as tk
   from tkinter import filedialog
   import xml.etree.ElementTree as ET
   from datetime import datetime
```
This class creates a scrollable frame in the GUI that allows the user to navigate through multiple checkboxes for column selection and easily add new columns if necessary.

#### Function to Convert TBX to HTML

```
   def convert_tbx_to_html(tbx_file_path, html_file_path, selected_columns):
    ...
```
This function parses the TBX file and converts its content to an HTML file, including only the selected columns. It constructs an HTML structure with tables and other HTML elements.

#### Function to Preview Columns

```
   def preview_columns(file_path, selected_columns):
    ...
```
This function reads the TBX file to identify and preview available columns. It returns a list of columns present in the file.

#### Function to Choose File

```
   def choose_file():
    ...
```
This function displays a GUI window with checkboxes for each column, allowing the user to select which columns to include in the HTML conversion.

#### GUI Main Window

```
   root = tk.Tk()
   root.title("Termfinder by User Assistance")
   root.geometry("500x150")
   ...
   root.mainloop()
```
This section sets up the main GUI window with buttons to choose a file and close the program. It also includes a label for informational text.


### Part 2: JavaScript for Enhanced HTML Functionality
The generated HTML file includes embedded JavaScript to provide interactive features such as filtering, toggling between languages, tooltips, and converting URLs to links.

#### Autocomplete Suggestions

```
   var autocompleteInput = document.getElementById('searchInput');
   if (suggestions.length > 0) {
      autocompleteInput.placeholder = suggestions[0].substring(filter.length);
   } else {
      autocompleteInput.placeholder = '';
   }
```
This section of the code dynamically updates the placeholder text in the input field based on the user's input. It shows autocomplete suggestions by displaying the first suggestion that matches the input, helping users to quickly find relevant terms.

#### Window Onload Event

```
   window.onload = function() {
    filterTable();
    toggleTable();
    addTooltipsFromTable();
    convertUrlsToLinks();
}
```
The window.onload event ensures that certain functions are executed only after the entire webpage has finished loading. This includes filtering the table, toggling the table language, adding tooltips, and converting URLs into clickable links.

#### Filter Table Function

```
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

        if (languageFilterPassed && filterFilterPassed) {
            rows[i].classList.remove('hidden');
        } else {
            rows[i].classList.add('hidden');
        }
    }
}
```
The filterTable function filters the table rows based on the selected language and filter criteria. It retrieves the selected values from dropdowns and compares them with the table data, showing only the rows that match the criteria and hiding the others.

#### Toggle Table Function

```
   function toggleTable() {
    var germanTable = document.getElementById('german-table');
    var englishTable = document.getElementById('english-table');

    if (document.getElementById('language-toggle').checked) {
        germanTable.style.display = 'table';
        englishTable.style.display = 'none';
    } else {
        germanTable.style.display = 'none';
        englishTable.style.display = 'table';
    }
}
```
The toggleTable function switches between displaying the German and English versions of the table. It checks the state of a checkbox and toggles the visibility of the respective tables accordingly, allowing users to view the information in their preferred language.

#### Tooltips Function

```
   function addTooltipsFromTable() {
    var tooltipTable = [
        ["Hauptbenennung", "Main term designation", "This is the main term designation."],
        ...
    ];

    var termTable = document.getElementById("termTable");
    var cells = termTable.getElementsByTagName("td");

    for (var i = 0; i < cells.length; i++) {
        var term = cells[i].innerText.trim();
        for (var j = 0; j < tooltipTable.length; j++) {
            if (tooltipTable[j][0] === term) {
                cells[i].classList.add("tooltip");
                cells[i].innerHTML += '<span class="tooltiptext">' + tooltipTable[j][2] + '</span>';
            }
        }
    }
}
```
The addTooltipsFromTable function adds tooltips to table cells based on predefined terms. It searches for specific terms in the table and, if found, attaches a tooltip to the cell to provide additional context or explanation, enhancing user understanding.

#### Convert URLs to Links

```
   function convertUrlsToLinks() {
    var table = document.getElementById("termTable");

    if (table) {
        for (var i = 0; i < table.rows.length; i++) {
            for (var j = 0; j < table.rows[i].cells.length; j++) {
                var cellContent = table.rows[i].cells[j].innerHTML;

                if ((cellContent.includes("http://") || cellContent.includes("https://")) && !cellContent.includes("(translation)")) {
                    var link = document.createElement("a");
                    link.href = cellContent;
                    link.textContent = cellContent;
                    link.target = "_blank";
                    table.rows[i].cells[j].innerHTML = '';
                    table.rows[i].cells[j].appendChild(link);
                } else if (cellContent.includes("(translation)")) {
                    var parts = cellContent.split("(translation)");
                    var linkBefore = document.createElement("a");
                    linkBefore.href = parts[0];
                    linkBefore.textContent = parts[0];
                    linkBefore.target = "_blank";
                    var textNodeAfter = document.createTextNode("(translation)" + parts[1]);
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
```
The convertUrlsToLinks function scans the table for any cells containing URLs and converts these URLs into clickable links. This function also handles special cases where URLs are followed by "(translation)" text, ensuring the content is properly formatted and interactive.

### HTML Structure
The generated HTML includes two tables (German and English) with relevant term data. It also includes interactive elements like a checkbox to toggle between languages, and dropdowns for filtering terms based on language and other criteria. The script ensures the HTML output is dynamic and user-friendly.



## Support
If you have questions or problems, contact me here on GitHub. :)


