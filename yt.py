import yt_dlp
import os
import logging
from rich.console import Console
from rich.progress import Progress

console = Console()
default_storage_path = "/sdcard/Download"
log_file = "download_log.txt"

# Setup logging
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def check_storage_access(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        return True
    except PermissionError:
        console.print("[red]Storage access denied. Check your permissions.[/red]")
        return False

def get_video_audio_info(url):
    try:
        console.print("Checking video URL...")
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            video_streams = [s for s in info['formats'] if s.get('vcodec') != 'none' and s.get('height') is not None]
            audio_streams = [s for s in info['formats'] if s.get('acodec') != 'none' and s.get('abr') is not None]

            max_video_res = max(video_streams, key=lambda x: x.get('height', 0)) if video_streams else None
            max_audio_bitrate = max(audio_streams, key=lambda x: x.get('abr', 0)) if audio_streams else None
            estimated_size = sum(f.get('filesize', 0) for f in video_streams if f.get('filesize')) // (1024 ** 2)

            return {
                'title': info.get('title'),
                'max_video_res': max_video_res.get('height') if max_video_res else 'No video available',
                'max_audio_bitrate': max_audio_bitrate.get('abr') if max_audio_bitrate else 'No audio available',
                'estimated_size': estimated_size if estimated_size > 0 else 'Unknown',
            }
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        logging.error(f"Error fetching video/audio info: {e}")
        return None

def download_video_or_audio(url, retries=3, custom_path=None):
    """Download video or audio from a YouTube URL."""
    storage_path = custom_path if custom_path else default_storage_path

    if not check_storage_access(storage_path):
        console.print("[red]Storage access failed. Ensure permissions are granted.[/red]")
        return

    info = get_video_audio_info(url)
    if not info:
        return

    console.print(f"\nTitle: {info['title']}")
    console.print(f"Max Video Resolution: {info['max_video_res']}p")
    console.print(f"Max Audio Bitrate: {info['max_audio_bitrate']} kbps")
    console.print(f"Estimated Size: {info['estimated_size']} MB\n")

    console.print("===  Format Options ===")
    console.print("[1] MP3 (Audio)")
    console.print("[2] WAV (Audio)")
    console.print("[3] MP4 (Video)")
    console.print("[4] WEBM (Video)")

    choice = input("Choose format (1/2/3/4): ").strip()
    quality = input("Enter quality (e.g., 192 for audio, 360/720 for video): ").strip()

    ydl_opts = {}
    if choice == "1":  # MP3
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': quality,
            }],
            'outtmpl': os.path.join(storage_path, '%(title)s.%(ext)s'),
        }
    elif choice == "2":  # WAV
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            }],
            'outtmpl': os.path.join(storage_path, '%(title)s.%(ext)s'),
        }
    elif choice == "3":  # MP4
        ydl_opts = {
            'format': f'bestvideo[height<={quality}]+bestaudio/best',
            'merge_output_format': 'mp4',
            'outtmpl': os.path.join(storage_path, '%(title)s.%(ext)s'),
        }
    elif choice == "4":  # WEBM
        ydl_opts = {
            'format': f'bestvideo[height<={quality}]+bestaudio/best',
            'merge_output_format': 'webm',
            'outtmpl': os.path.join(storage_path, '%(title)s.%(ext)s'),
        }
    else:
        console.print("[red]Invalid choice. Program terminated.[/red]")
        return

    for attempt in range(retries):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                console.print("[blue]Downloading...[/blue]")
                with Progress() as progress:
                    task = progress.add_task("Download Progress", total=100)

                    def hook(d):
                        if d['status'] == 'downloading':
                            percentage = float(d.get('_percent_str', '0.0').strip('%'))
                            progress.update(task, completed=percentage)
                        elif d['status'] == 'finished':
                            progress.update(task, completed=100)

                    ydl_opts['progress_hooks'] = [hook]
                    ydl.download([url])

            console.print("[green]Download complete![/green]")
            logging.info(f"Successfully downloaded: {info['title']}")
            return
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            logging.error(f"Error during download (Attempt {attempt + 1}/{retries}): {e}")
            if attempt + 1 < retries:
                console.print(f"[yellow]Retrying... ({attempt + 1}/{retries})[/yellow]")

    console.print("[red]Failed to download after multiple attempts.[/red]")

def batch_download(custom_path=None):
    """Batch download mode for downloading multiple URLs."""
    console.print("[cyan]Batch Download Mode[/cyan]")
    urls = input("Enter YouTube URLs separated by commas: ").strip().split(',')
    for url in urls:
        download_video_or_audio(url.strip(), custom_path=custom_path)

if __name__ == "__main__":
    mode = input("Choose mode (1: Single Download, 2: Batch Download): ").strip()
    custom_path = input("Enter custom save path (leave blank for default): ").strip()
    custom_path = custom_path if custom_path else None

    if mode == "1":
        video_url = input("Enter YouTube URL: ").strip()
        download_video_or_audio(video_url, custom_path=custom_path)
    elif mode == "2":
        batch_download(custom_path=custom_path)
    else:
        console.print("[red]Invalid choice![/red]")
