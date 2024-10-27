import os
from pytubefix import YouTube
from pytubefix.cli import on_progress
from moviepy.editor import VideoFileClip, AudioFileClip
from concurrent.futures import ThreadPoolExecutor, wait

url = input("Copie aqui o link do vídeo do YouTube que deseja baixar: ")
reso = YouTube(url)

def download(reso):
    if reso.streams.get_by_itag(137):
        yt = YouTube(url, on_progress_callback=on_progress)
        print(yt.title)
        yt.streams.filter(res="1080p").first().download(filename="video.mp4")

    elif reso.streams.get_by_itag(136):
        yt = YouTube(url, on_progress_callback=on_progress)
        print(yt.title)
        yt.streams.filter(res="720p").first().download(filename="video.mp4")

    elif reso.streams.get_by_itag(135):
        yt = YouTube(url, on_progress_callback=on_progress)
        print(yt.title)
        yt.streams.filter(res="480p").first().download(filename="video.mp4")  

    elif reso.streams.get_by_itag(134):
        yt = YouTube(url, on_progress_callback=on_progress)
        print(yt.title)
        yt.streams.filter(res="360p").first().download(filename="video.mp4")

    elif reso.streams.get_by_itag(133):
        yt = YouTube(url, on_progress_callback=on_progress)
        print(yt.title)
        yt.streams.filter(res="240p").first().download(filename="video.mp4") 
    else:
        print("Desculpe! O vídeo não possui nenhuma qualidade suportada!")

# Função para baixar o áudio
def audio_mp3(url):
    yt = YouTube(url, on_progress_callback=on_progress)
    print(yt.title)
    audio = yt.streams.get_audio_only()
    audio.download(filename="audio.mp3")  # Corrigido para baixar em mp3

# Função para combinar áudio e vídeo
def final_video(video, audio, output_title):
    video_clip = VideoFileClip(video)
    audio_clip = AudioFileClip(audio)

    final_clip = video_clip.set_audio(audio_clip)

    # Melhorar a velocidade ajustando o codec e threads
    final_clip.write_videofile(f"{output_title}.mp4", codec="libx264", threads=4, preset="ultrafast")

    # Liberando os recursos
    video_clip.close()
    audio_clip.close()
    final_clip.close()

    # Remover arquivos temporários de vídeo e áudio
    os.remove(video)
    os.remove(audio)
    print("Arquivos temporários removidos.")

# Usar o título do vídeo como nome final do arquivo de saída
output_title = reso.title

# Executor para download e processamento paralelo
with ThreadPoolExecutor() as executor:
    future1 = executor.submit(download, reso)
    future2 = executor.submit(audio_mp3, url)

    # Esperando ambas funções terminarem
    wait([future1, future2])

    # Criando o vídeo final após os downloads
    final_video("video.mp4", "audio.mp3", output_title)






