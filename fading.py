import pyttsx3
import os

def text_to_speech(text, output_file):
    # Inicialize o motor TTS
    engine = pyttsx3.init()
    
    # Defina a taxa de fala (velocidade)
    engine.setProperty('rate', 150)  # Ajuste para uma taxa moderada
    
    # Defina o volume
    engine.setProperty('volume', 1.0)  # Defina o volume máximo
    
    # Listar todas as vozes disponíveis
    voices = engine.getProperty('voices')
    
    # Escolha uma voz diferente se disponível
    for voice in voices:
        if "brazil" in voice.name.lower():  # Procure por uma voz brasileira (ou ajuste conforme necessário)
            engine.setProperty('voice', voice.id)
            break
    else:
        # Se não encontrar uma voz específica, use a primeira disponível
        engine.setProperty('voice', voices[0].id)
    
    # Converta texto em fala e salve em arquivo WAV
    engine.save_to_file(text, output_file)
    
    # Também toque o texto
    engine.say(text)
    
    # Execute o processo de conversão e reprodução
    engine.runAndWait()

if __name__ == "__main__":
    # Texto a ser convertido em fala
    text = ("Bom dia brabona, esse é um exemplo de conversão de texto para áudio usando paiton. "
            "Acabei de descobrir como funciona esse treco e achei muito legal. beijos para você")
    
    # Nome do arquivo de saída
    output_file = "recado.wav"
    
    # Chame a função para converter texto em fala, tocar e salvar em arquivo
    text_to_speech(text, output_file)
    
    # Confirme que o arquivo foi salvo
    if os.path.exists(output_file):
        print(f"O arquivo de áudio foi salvo como {output_file}")
    else:
        print("Falha ao salvar o arquivo de áudio.")
