from gtts import gTTS
import os
from playsound import playsound

def text_to_speech(text, output_file):
    # Definir o idioma (por exemplo, 'pt' para português, 'en' para inglês, 'es' para espanhol, etc.)
    language = 'de'
    
    # Converter texto em fala usando gTTS
    tts = gTTS(text=text, lang=language, slow=False)
    
    # Salvar o áudio em um arquivo MP3
    tts.save(output_file)
    
    # Reproduzir o áudio
    playsound(output_file)

if __name__ == "__main__":
    # Texto a ser convertido em fala
    text = ("Alemão purro ou alemão de luxemburgo?"
            "")
    
    # Nome do arquivo de saída
    output_file = "racao.mp3"
    
    # Chame a função para converter texto em fala, salvar em arquivo e reproduzir
    text_to_speech(text, output_file)
    
    # Confirme que o arquivo foi salvo
    if os.path.exists(output_file):
        print(f"O arquivo de áudio foi salvo como {output_file}")
    else:
        print("Falha ao salvar o arquivo de áudio.")
