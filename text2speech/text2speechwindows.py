import pyttsx3
import os
from pydub import AudioSegment

def text_to_speech(text, output_wav, output_mp3):
    # Inicialize o motor TTS
    engine = pyttsx3.init()
    
        # Obtenha todas as vozes disponíveis
    voices = engine.getProperty('voices')
    
    # Defina a taxa de fala (velocidade)
    engine.setProperty('rate', 200)  # Ajuste para uma taxa moderada
    
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
    engine.save_to_file(text, output_wav)
    
    # Também toque o texto
    engine.say(text)
    
    # Execute o processo de conversão e reprodução
    engine.runAndWait()
    
    # Converter WAV para MP3 usando pydub
    sound = AudioSegment.from_wav(output_wav)
    sound.export(output_mp3, format="mp3")
    
    # Confirme que o arquivo foi salvo
    if os.path.exists(output_mp3):
        print(f"O arquivo de áudio foi salvo como {output_mp3}")
    else:
        print("Falha ao salvar o arquivo de áudio.")
        
def list_available_voices():
    # Inicialize o motor TTS
    engine = pyttsx3.init()
    
    # Obtenha todas as vozes disponíveis
    voices = engine.getProperty('voices')
    
    # Listar todas as vozes com seus detalhes
    for voice in voices:
        print(f"ID: {voice.id}")
        print(f"Name: {voice.name}")
        print(f"Languages: {voice.languages}")
        print(f"Gender: {voice.gender}")
        print(f"Age: {voice.age}")
        print()

if __name__ == "__main__":
    
    list_available_voices()
    
    # Texto a ser convertido em fala
    text = ("Que tal uma empanada. "
            "Uma especial, de alta raridade, de 58 Hertz. ")
    
    # Nomes dos arquivos de saída
    output_wav = "recado.wav"
    output_mp3 = "recado.mp3"
    
    # Chame a função para converter texto em fala, tocar e salvar em arquivos WAV e MP3
    text_to_speech(text, output_wav, output_mp3)
