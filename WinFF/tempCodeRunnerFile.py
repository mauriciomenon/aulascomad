import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import configparser
import json
import threading
import platform

# Caminho padrão em subpasta bin para o ffmpeg
def get_default_ffmpeg_path():
    executable_name = 'ffmpeg.exe' if platform.system() == 'Windows' else 'ffmpeg'
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bin', executable_name)

# Inicializar o objeto de configuração
config = configparser.ConfigParser()
config_file = 'config.ini'

# Carregar ou criar configuração
def load_or_create_config():
    if os.path.exists(config_file):
        config.read(config_file)
    else:
        config['DEFAULT'] = {
            'ffmpeg_path': get_default_ffmpeg_path(),
            'default_format': 'wmv',
            'default_output_dir': '',
            'default_video_codec': 'wmv2',
            'default_audio_codec': 'wmav2',
            'default_resolution': '320x240',
            'video_bitrate': '204800',
            'audio_bitrate': '65536',
            'frame_rate': '20',
            'audio_sample_rate': '22050',
            'audio_channels': '1',
            'use_same_directory': 'False',
            'overwrite_existing': 'True'
        }
        with open(config_file, 'w') as configfile:
            config.write(configfile)

load_or_create_config()

# Função para carregar configurações
def load_config(file_name):
    config.read(file_name)
    apply_saved_config()

# Função para salvar configurações
def save_config():
    config_file_path = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Salvar Configuração", defaultextension=".ini", filetypes=[("Arquivos INI", "*.ini")])
    if not config_file_path:
        messagebox.showwarning("Atenção", "Nenhum arquivo selecionado. Configuração não salva.")
        return

    config['DEFAULT'] = {
        'ffmpeg_path': ffmpeg_path_entry.get(),
        'default_format': format_var.get(),
        'default_output_dir': output_dir_entry.get(),
        'default_video_codec': video_codec_var.get(),
        'default_audio_codec': audio_codec_var.get(),
        'default_resolution': resolution_var.get(),
        'video_bitrate': video_bitrate_entry.get(),
        'audio_bitrate': audio_bitrate_entry.get(),
        'frame_rate': frame_rate_entry.get(),
        'audio_sample_rate': audio_sample_rate_entry.get(),
        'audio_channels': audio_channels_var.get(),
        'use_same_directory': use_same_directory_var.get(),
        'overwrite_existing': overwrite_var.get()
    }
    with open(config_file_path, 'w') as configfile:
        config.write(configfile)
    messagebox.showinfo("Configuração", f"Configuração salva com sucesso em {config_file_path}.")

# Função para definir configurações padrão
def set_default_options():
    format_var.set("wmv")
    resolution_var.set("320x240")
    video_codec_var.set("wmv2")
    audio_codec_var.set("wmav2")
    video_bitrate_entry.delete(0, tk.END)
    video_bitrate_entry.insert(0, "204800")
    audio_bitrate_entry.delete(0, tk.END)
    audio_bitrate_entry.insert(0, "65536")
    frame_rate_entry.delete(0, tk.END)
    frame_rate_entry.insert(0, "20")
    audio_sample_rate_entry.delete(0, tk.END)
    audio_sample_rate_entry.insert(0, "22050")
    audio_channels_var.set("1")
    output_dir_entry.delete(0, tk.END)
    ffmpeg_path_entry.delete(0, tk.END)
    ffmpeg_path_entry.insert(0, get_default_ffmpeg_path())
    use_same_directory_var.set(False)
    overwrite_var.set(True)
    update_command_display()

# Função para aplicar opções salvas
def apply_saved_config():
    ffmpeg_path_entry.delete(0, tk.END)
    ffmpeg_path_entry.insert(0, config.get('DEFAULT', 'ffmpeg_path', fallback=get_default_ffmpeg_path()))
    output_dir_entry.delete(0, tk.END)
    output_dir_entry.insert(0, config.get('DEFAULT', 'default_output_dir', fallback=''))
    format_var.set(config.get('DEFAULT', 'default_format', fallback='wmv'))
    video_codec_var.set(config.get('DEFAULT', 'default_video_codec', fallback='wmv2'))
    audio_codec_var.set(config.get('DEFAULT', 'default_audio_codec', fallback='wmav2'))
    resolution_var.set(config.get('DEFAULT', 'default_resolution', fallback='320x240'))
    video_bitrate_entry.delete(0, tk.END)
    video_bitrate_entry.insert(0, config.get('DEFAULT', 'video_bitrate', fallback='204800'))
    audio_bitrate_entry.delete(0, tk.END)
    audio_bitrate_entry.insert(0, config.get('DEFAULT', 'audio_bitrate', fallback='65536'))
    frame_rate_entry.delete(0, tk.END)
    frame_rate_entry.insert(0, config.get('DEFAULT', 'frame_rate', fallback='20'))
    audio_sample_rate_entry.delete(0, tk.END)
    audio_sample_rate_entry.insert(0, config.get('DEFAULT', 'audio_sample_rate', fallback='22050'))
    audio_channels_var.set(config.get('DEFAULT', 'audio_channels', fallback='1'))
    use_same_directory_var.set(config.getboolean('DEFAULT', 'use_same_directory', fallback=False))
    overwrite_var.set(config.getboolean('DEFAULT', 'overwrite_existing', fallback=True))
    toggle_output_directory()
    update_command_display()

# Função para selecionar arquivos de vídeo
def select_files():
    files = filedialog.askopenfilenames(title="Selecione os arquivos de vídeo")
    if files:
        current_files = file_list.get(0, tk.END)
        for file in files:
            if file not in current_files:
                file_list.insert(tk.END, file)
    update_command_display()

# Função para selecionar diretório de saída
def select_output_directory():
    directory = filedialog.askdirectory(title="Selecione o diretório de saída")
    output_dir_entry.delete(0, tk.END)
    output_dir_entry.insert(0, directory)
    update_command_display()

# Função para selecionar o executável do FFmpeg
def select_ffmpeg_executable():
    ffmpeg_path = filedialog.askopenfilename(title="Selecione o Executável FFmpeg", filetypes=[("Executáveis", "*.*")])
    ffmpeg_path_entry.delete(0, tk.END)
    ffmpeg_path_entry.insert(0, ffmpeg_path)
    config['DEFAULT']['ffmpeg_path'] = ffmpeg_path
    with open(config_file, 'w') as configfile:
        config.write(configfile)
    update_command_display()

# Função para carregar uma configuração
def load_config_from_file():
    config_file = filedialog.askopenfilename(title="Carregar Configuração", filetypes=[("Configurações", "*.ini")])
    if config_file:
        load_config(config_file)
        messagebox.showinfo("Carregar Configuração", "Configuração carregada com sucesso!")

# Função para converter vídeos em lote
def convert_videos():
    files = file_list.get(0, tk.END)
    if not files:
        messagebox.showwarning("Atenção", "Nenhum arquivo de vídeo selecionado.")
        return

    ffmpeg_path = ffmpeg_path_entry.get()
    if not os.path.exists(ffmpeg_path):
        messagebox.showerror("Erro", "Caminho do FFmpeg não encontrado. Verifique se o caminho está correto.")
        return

    output_format = format_var.get()
    video_bitrate = video_bitrate_entry.get()
    audio_bitrate = audio_bitrate_entry.get()
    resolution = resolution_var.get()
    video_codec = video_codec_var.get()
    audio_codec = audio_codec_var.get()
    frame_rate = frame_rate_entry.get()
    audio_sample_rate = audio_sample_rate_entry.get()
    audio_channels = audio_channels_var.get()

    def run_conversion():
        total_files = len(files)
        total_progress['maximum'] = total_files
        total_progress['value'] = 0

        for index, input_file in enumerate(files):
            if use_same_directory_var.get():
                output_dir = os.path.dirname(input_file)
            else:
                output_dir = output_dir_entry.get()

            if not output_dir:
                messagebox.showwarning("Erro de Entrada", "Por favor, selecione um diretório de saída.")
                return

            output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file))[0] + '.' + output_format)

            if not overwrite_var.get() and os.path.exists(output_file):
                messagebox.showerror("Erro", f"O arquivo '{output_file}' já existe e não pode ser sobrescrito.")
                return

            command = [
                ffmpeg_path, '-y', '-i', input_file,
                '-b:v', video_bitrate,
                '-b:a', audio_bitrate,
                '-s', resolution,
                '-r', frame_rate,
                '-ar', audio_sample_rate,
                '-ac', audio_channels,
                '-vcodec', video_codec,
                '-acodec', audio_codec,
                output_file
            ]

            individual_progress['maximum'] = 100
            individual_progress['value'] = 0

            try:
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

                while True:
                    output = process.stderr.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        root.update_idletasks()

                process.wait()

            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao converter vídeo.\nErro: {e}")
                return

            total_progress['value'] += 1
            individual_progress['value'] = 100
            root.update_idletasks()

        messagebox.showinfo("Sucesso", "Conversão de vídeos concluída.")

    conversion_thread = threading.Thread(target=run_conversion)
    conversion_thread.start()

# Função para atualizar a exibição do comando FFmpeg
def update_command_display():
    files = file_list.get(0, tk.END)
    if not files:
        command_display.delete(1.0, tk.END)
        return

    first_file = files[0]
    output_format = format_var.get()
    video_bitrate = video_bitrate_entry.get()
    audio_bitrate = audio_bitrate_entry.get()
    resolution = resolution_var.get()
    video_codec = video_codec_var.get()
    audio_codec = audio_codec_var.get()
    frame_rate = frame_rate_entry.get()
    audio_sample_rate = audio_sample_rate_entry.get()
    audio_channels = audio_channels_var.get()
    ffmpeg_path = ffmpeg_path_entry.get()

    if use_same_directory_var.get():
        output_dir = os.path.dirname(first_file)
    else:
        output_dir = output_dir_entry.get()

    output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(first_file))[0] + '.' + output_format)

    command = f"\"{ffmpeg_path}\" -y -i \"{first_file}\""

    if video_bitrate:
        command += f" -b:v {video_bitrate}"

    if audio_bitrate:
        command += f" -b:a {audio_bitrate}"

    if resolution != "original":
        command += f" -s {resolution}"

    if frame_rate:
        command += f" -r {frame_rate}"

    if audio_sample_rate:
        command += f" -ar {audio_sample_rate}"

    if audio_channels:
        command += f" -ac {audio_channels}"

    if video_codec != "auto":
        command += f" -vcodec {video_codec}"

    if audio_codec != "auto":
        command += f" -acodec {audio_codec}"

    command += f" \"{output_file}\""
    
    command_display.delete(1.0, tk.END)
    command_display.insert(tk.END, command)

# Função para alternar a habilitação do campo de diretório de saída
def toggle_output_directory():
    if use_same_directory_var.get():
        output_dir_entry.config(state=tk.DISABLED)
        output_dir_button.config(state=tk.DISABLED)
    else:
        output_dir_entry.config(state=tk.NORMAL)
        output_dir_button.config(state=tk.NORMAL)
    update_command_display()

# Função para exibir informações sobre o programa
def show_about():
    messagebox.showinfo("About", "Mauricio Menon (+AI) \ngithub.com/mauriciomenon\nPython 3.10 + tk \nVersão 8.3.0 \n07/08/2024")

# Função para exibir informações do arquivo de vídeo
def show_video_info():
    selected_files = file_list.curselection()
    if not selected_files:
        messagebox.showwarning("Atenção", "Nenhum arquivo de vídeo selecionado.")
        return

    input_file = file_list.get(selected_files[0])
    ffmpeg_path = ffmpeg_path_entry.get()
    ffprobe_path = os.path.join(os.path.dirname(ffmpeg_path), 'ffprobe' if platform.system() == 'Darwin' else 'ffprobe.exe')

    if not os.path.exists(ffprobe_path):
        messagebox.showerror("Erro", "Caminho do ffprobe não encontrado. Verifique se o caminho está correto.")
        return

    try:
        command = [ffprobe_path, '-v', 'quiet', '-print_format', 'json', '-show_streams', '-show_format', input_file]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        if process.returncode != 0:
            raise Exception(f'Erro ao executar ffprobe: {err}')

        info_data = json.loads(out)
        info_text = f"Informações do Arquivo: {os.path.basename(input_file)}\n\n"
        audio_count = 0
        for stream in info_data.get('streams', []):
            if stream['codec_type'] == 'video':
                info_text += "Stream de Vídeo\n"
                info_keys = ['codec_long_name', 'display_aspect_ratio', 'width', 'height', 'r_frame_rate']
            elif stream['codec_type'] == 'audio':
                audio_count += 1
                info_text += f"Stream de Áudio {audio_count}\n"
                info_keys = ['codec_long_name', 'channels', 'sample_rate', 'bit_rate']

            for key in info_keys:
                if key in stream:
                    value = stream[key]
                    if key == 'codec_long_name':
                        description = "Codec"
                    elif key == 'display_aspect_ratio':
                        description = "Proporção de Exibição"
                    elif key == 'width':
                        description = "Largura"
                        value = f"{value} pixels"
                    elif key == 'height':
                        description = "Altura"
                        value = f"{value} pixels"
                    elif key == 'channels':
                        description = "Canais"
                        value = f"{value} ({'mono' if value == '1' else 'stereo' if value == '2' else 'multi-channel'})"
                    elif key == 'sample_rate':
                        description = "Taxa de Amostragem"
                        value += " Hz"
                    elif key == 'r_frame_rate':
                        description = "FPS"
                    elif key == 'bit_rate':
                        description = "Taxa de Bits"
                        value = f"{int(value)/1000:.2f} kbps"
                    info_text += f"{description}: {value}\n"
            info_text += "\n"

        if 'format' in info_data:
            info_text += "Informações do Formato\n"
            for key in ['format_name', 'duration', 'size', 'bit_rate']:
                if key in info_data['format']:
                    value = info_data['format'][key]
                    if key == 'format_name':
                        description = "Formato"
                    elif key == 'duration':
                        description = "Duração"
                        value = f"{float(value):.2f} segundos"
                    elif key == 'size':
                        description = "Tamanho"
                        value = f"{int(value)/1024/1024:.2f} MB"
                    elif key == 'bit_rate':
                        description = "Taxa de Bits"
                        value = f"{int(value)/1000:.2f} kbps"
                    info_text += f"{description}: {value}\n"

        # Criação da janela de informações copiáveis
        info_window = tk.Toplevel()
        info_window.title("Informações Detalhadas do Vídeo")
        text_widget = tk.Text(info_window, wrap='word', height=30, width=80)
        text_widget.insert('end', info_text)
        text_widget.pack(side='top', fill='both', expand=True)
        text_widget.config(state='normal')  # Permite edição para facilitar a cópia
        tk.Button(info_window, text="Fechar", command=info_window.destroy).pack(side='bottom')
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível obter informações do vídeo.\nErro: {str(e)}")

# Criar janela principal
root = tk.Tk()
root.title("Conversor de Vídeo Avançado")

# Ajustar o tamanho da janela com base no sistema operacional
if platform.system() == "Darwin":  # macOS
    root.geometry("1200x850")
else:  # Windows
    root.geometry("820x650")

# Botão "About" e "Info" na mesma linha
about_button = tk.Button(root, text="Sobre o Programa", command=show_about, font=("TkDefaultFont", 9))
about_button.grid(row=1, column=2, padx=5, pady=5, sticky="e")
info_button = tk.Button(root, text="Codecs do vídeo", command=show_video_info, font=("TkDefaultFont", 9))
info_button.grid(row=1, column=3, padx=5, pady=5, sticky="w")

# Lista de arquivos
tk.Label(root, text="Arquivos Selecionados:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
file_list = tk.Listbox(root, width=80, height=8, selectmode=tk.MULTIPLE)
file_list.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="we")

# Botões para adicionar e remover arquivos
add_button = tk.Button(root, text="Adicionar Arquivos", command=select_files)
add_button.grid(row=2, column=2, padx=5, pady=5, sticky="e")
remove_button = tk.Button(root, text="Remover Arquivo", command=lambda: file_list.delete(tk.ANCHOR))
remove_button.grid(row=2, column=3, padx=5, pady=5, sticky="w")

# Diretório de saída
tk.Label(root, text="Diretório de Saída:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
output_dir_entry = tk.Entry(root, width=70)
output_dir_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="we")
output_dir_button = tk.Button(root, text="Procurar", command=select_output_directory)
output_dir_button.grid(row=3, column=3, padx=5, pady=5)

# Caixa de seleção para usar o mesmo diretório do arquivo de vídeo
use_same_directory_var = tk.BooleanVar()
use_same_directory_check = tk.Checkbutton(root, text="Usar mesmo diretório do arquivo de entrada", variable=use_same_directory_var, command=toggle_output_directory)
use_same_directory_check.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="w")

# Checkbox para sobrescrever arquivos
overwrite_var = tk.BooleanVar()
overwrite_check = tk.Checkbutton(root, text="Sobrescrever arquivos existentes", variable=overwrite_var)
overwrite_check.grid(row=4, column=2, columnspan=2, padx=5, pady=5, sticky="w")

# Formato de saída
tk.Label(root, text="Formato de Saída:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
format_var = tk.StringVar()
format_menu = tk.OptionMenu(root, format_var, "mp4", "avi", "mkv", "flv", "mov", "mp3", "wmv")
format_menu.grid(row=5, column=1, padx=5, pady=5, sticky="w")

# Bitrate de vídeo
tk.Label(root, text="Bitrate de Vídeo (ex.: 204800):").grid(row=6, column=0, padx=5, pady=5, sticky="w")
video_bitrate_entry = tk.Entry(root, width=20)
video_bitrate_entry.grid(row=6, column=1, padx=5, pady=5, sticky="w")

# Bitrate de áudio
tk.Label(root, text="Bitrate de Áudio (ex.: 65536):").grid(row=6, column=2, padx=5, pady=5, sticky="w")
audio_bitrate_entry = tk.Entry(root, width=20)
audio_bitrate_entry.grid(row=6, column=3, padx=5, pady=5, sticky="w")

# Resolução
tk.Label(root, text="Resolução:").grid(row=7, column=0, padx=5, pady=5, sticky="w")
resolution_var = tk.StringVar()
resolution_menu = tk.OptionMenu(root, resolution_var, "original", "1920x1080", "1280x720", "640x480", "320x240")
resolution_menu.grid(row=7, column=1, padx=5, pady=5, sticky="w")

# Codec de vídeo
tk.Label(root, text="Codec de Vídeo:").grid(row=7, column=2, padx=5, pady=5, sticky="w")
video_codec_var = tk.StringVar()
video_codec_menu = tk.OptionMenu(root, video_codec_var, "auto", "libx264", "libx265", "mpeg4", "wmv2")
video_codec_menu.grid(row=7, column=3, padx=5, pady=5, sticky="w")

# Codec de áudio
tk.Label(root, text="Codec de Áudio:").grid(row=8, column=0, padx=5, pady=5, sticky="w")
audio_codec_var = tk.StringVar()
audio_codec_menu = tk.OptionMenu(root, audio_codec_var, "auto", "aac", "mp3", "ac3", "wmav2")
audio_codec_menu.grid(row=8, column=1, padx=5, pady=5, sticky="w")

# Taxa de quadros
tk.Label(root, text="Taxa de Quadros (ex.: 20):").grid(row=8, column=2, padx=5, pady=5, sticky="w")
frame_rate_entry = tk.Entry(root, width=20)
frame_rate_entry.grid(row=8, column=3, padx=5, pady=5, sticky="w")

# Taxa de amostragem de áudio
tk.Label(root, text="Taxa de Amostragem de Áudio (ex.: 22050):").grid(row=9, column=0, padx=5, pady=5, sticky="w")
audio_sample_rate_entry = tk.Entry(root, width=20)
audio_sample_rate_entry.grid(row=9, column=1, padx=5, pady=5, sticky="w")

# Canais de áudio
tk.Label(root, text="Canais de Áudio:").grid(row=9, column=2, padx=5, pady=5, sticky="w")
audio_channels_var = tk.StringVar()
audio_channels_menu = tk.OptionMenu(root, audio_channels_var, "1", "2")
audio_channels_menu.grid(row=9, column=3, padx=5, pady=5, sticky="w")

# Caminho do FFmpeg
tk.Label(root, text="Caminho do FFmpeg:").grid(row=10, column=0, padx=5, pady=5, sticky="w")
ffmpeg_path_entry = tk.Entry(root, width=70)
ffmpeg_path_entry.grid(row=10, column=1, columnspan=2, padx=5, pady=5, sticky="we")
tk.Button(root, text="Procurar", command=select_ffmpeg_executable).grid(row=10, column=3, padx=5, pady=5)

# Caixa do comando do FFmpeg
tk.Label(root, text="Comando FFmpeg:").grid(row=11, column=0, padx=5, pady=5, sticky="nw")
command_display = tk.Text(root, height=4, width=70, font=("TkDefaultFont", 9))
command_display.grid(row=11, column=1, columnspan=3, padx=5, pady=5, sticky="we")

# Barra de progresso total
total_progress = ttk.Progressbar(root, orient="horizontal", mode="determinate")
total_progress.grid(row=12, column=0, columnspan=2, padx=5, pady=5, sticky="we")

# Barra de progresso individual
individual_progress = ttk.Progressbar(root, orient="horizontal", mode="determinate")
individual_progress.grid(row=12, column=2, columnspan=2, padx=5, pady=5, sticky="we")

# Botão para aplicar opções padrão
default_button = tk.Button(root, text="Opções Padrão", command=set_default_options)
default_button.grid(row=13, column=0, padx=5, pady=5, sticky="we")

# Botão para carregar opções salvas
load_button = tk.Button(root, text="Carregar Configuração", command=load_config_from_file)
load_button.grid(row=13, column=1, padx=5, pady=5, sticky="we")

# Botão para salvar configurações
save_button = tk.Button(root, text="Salvar Configuração", command=save_config)
save_button.grid(row=13, column=2, padx=5, pady=5, sticky="we")

# Botão para converter vídeos
convert_button = tk.Button(root, text="Converter", command=convert_videos, font=("TkDefaultFont", 11, "bold"))
convert_button.grid(row=13, column=3, padx=5, pady=5, sticky="we")

# Aplicar configurações padrão no início, sem exibir mensagem
set_default_options()

# Executar o loop principal da interface
root.mainloop()