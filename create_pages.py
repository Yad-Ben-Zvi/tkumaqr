import csv
import os
import qrcode

# Define the directory for HTML files
html_dir = 'html'
os.makedirs(html_dir, exist_ok=True)

# Read the template HTML file
with open('template.html', 'r', encoding='utf-8') as template_file:
    template_content = template_file.read()

# Prepare the index.html content
index_content = "<html dir='rtl'><body><h1>קוד QR לתקומה - הדגמה</h1>"

# Read the cleaned CSV file
with open('export_clean.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    for row in csv_reader:
        # Create a filename for each item using the Object identifier
        object_id = row['Object identifier']
        filename = f"{object_id}.html"
        filepath = os.path.join(html_dir, filename)
        
        # Replace placeholders in the template with actual data
        item_content = template_content
        for key, value in row.items():
            placeholder = f"{{{{ {key} }}}}"
            item_content = item_content.replace(placeholder, value if value else 'N/A')
        
        # Write the HTML content to a file
        with open(filepath, 'w', encoding='utf-8') as html_file:
            html_file.write(item_content)
        
        # Generate a QR code for the HTML page
        url = f"https://yad-ben-zvi.github.io/tkumaqr/html/{filename}"
        qr = qrcode.make(url)
        qr_filename = f"{object_id}_qr.png"
        qr_filepath = os.path.join(html_dir, qr_filename)
        qr.save(qr_filepath)
        
        # Add the QR code to the index.html content
        index_content += f'<div style="display: inline-block; margin: 10px;"><a href="{url}">{object_id}</a><br><img src="{qr_filename}" alt="QR Code for {filename}"></div>'

# Finalize and write the index.html content
index_content += "</body></html>"
with open(os.path.join(html_dir, 'index.html'), 'w', encoding='utf-8') as index_file:
    index_file.write(index_content)

print("HTML pages and QR codes have been generated in the 'html' directory.")