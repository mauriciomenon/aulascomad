import PyPDF2
import csv

def extract_emails_from_pdf(pdf_filename):
    emails = []
    
    with open(pdf_filename, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        
        # Para cada página no PDF
        for page_num in range(reader.numPages):
            text = reader.getPage(page_num).extractText()
            # Divide o texto em linhas
            lines = text.split("\n")
            
            for line in lines:
                # Procura linhas que parecem ser e-mails
                if "@" in line:
                    emails.append(line.strip())
    
    return emails

def save_emails_to_csv(emails, csv_filename):
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Email"]) # Cabeçalho da coluna
        
        for email in emails:
            writer.writerow([email])

def main():
    pdf_filename = 'path_to_your_pdf_file.pdf'
    csv_filename = 'output_emails.csv'
    
    emails = extract_emails_from_pdf(pdf_filename)
    save_emails_to_csv(emails, csv_filename)

if __name__ == '__main__':
    main()
