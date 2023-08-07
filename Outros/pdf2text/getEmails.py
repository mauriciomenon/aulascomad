import PyPDF2
import re
import sys


def extract_emails_from_pdf(pdf_filename):
    emails = set()  # Utilizamos um conjunto para garantir e-mails únicos

    with open(pdf_filename, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        for page_num in range(len(reader.pages)):
            text = reader.pages[page_num].extract_text()
            lines = text.split("\n")

            for line in lines:
                match = re.search(r"([\w._%+-]+@[\w.-]+\.(com|com\.br))", line)
                if match:
                    emails.add(match.group(1))  # Adiciona o e-mail ao conjunto

    # Converte de volta para lista para manter o código restante consistente
    return list(emails)


def save_emails_to_txt(emails, txt_filename):
    with open(txt_filename, 'w') as txtfile:
        for email in emails:
            txtfile.write(email + '\n')


def main():
    if len(sys.argv) > 1:
        # Pega o caminho do arquivo do argumento na linha de comando
        pdf_filename = sys.argv[1]
    else:
        pdf_filename = input(
            "Por favor, insira o caminho completo para o arquivo PDF: ")

    txt_filename = pdf_filename.rsplit('.', 1)[0] + '.txt'

    print(
        f"Um arquivo de saída com o nome '{txt_filename}' será criado no mesmo diretório.")

    emails = extract_emails_from_pdf(pdf_filename)
    save_emails_to_txt(emails, txt_filename)

    print(f"Lista de emails salva em '{txt_filename}'.")


if __name__ == '__main__':
    main()