

import tkinter as tk
from tkinter import messagebox, ttk
import yt_dlp

def get_video_formats(url):
    # Options to fetch available formats without downloading
    ydl_opts = {
        'quiet': True,  # Suppress output
        'extract_flat': True,  # Don't download, just list available formats
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get('formats', [])
    return formats

def download_facebook_video(url, quality, output_path='.'):
    # Define the options for yt-dlp
    ydl_opts = {
        'format': quality,  # Download the selected quality format
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',  # Output file name pattern
        'quiet': False,  # Show download progress
    }

    try:
        # Using yt-dlp to download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            messagebox.showinfo("Success", "Download completed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def choose_video_quality(formats, quality_combobox):
    # Clear current quality options in the combobox
    quality_combobox.set('')
    quality_combobox['values'] = []

    # Add available quality options to the combobox
    quality_options = []
    for idx, fmt in enumerate(formats):
        quality_options.append(f"{fmt.get('format_note', 'Unknown')} - {fmt.get('width', 'N/A')}x{fmt.get('height', 'N/A')} - {fmt.get('ext', 'Unknown format')}")
    
    quality_combobox['values'] = quality_options
    if quality_options:
        quality_combobox.set(quality_options[0])  # Set default to first option

def on_download_button_click(video_url_entry, quality_combobox):
    video_url = video_url_entry.get()
    if not video_url:
        messagebox.showerror("Error", "Please enter a valid Facebook video URL.")
        return
    
    # Get available formats for the video
    formats = get_video_formats(video_url)

    if not formats:
        messagebox.showerror("Error", "No available formats found. The video might be private or unavailable.")
        return

    # Get selected quality from combobox
    selected_quality = quality_combobox.get()
    if not selected_quality:
        messagebox.showerror("Error", "Please select a video quality.")
        return

    # Map selected quality back to format ID
    selected_format_id = None
    for fmt in formats:
        fmt_str = f"{fmt.get('format_note', 'Unknown')} - {fmt.get('width', 'N/A')}x{fmt.get('height', 'N/A')} - {fmt.get('ext', 'Unknown format')}"
        if fmt_str == selected_quality:
            selected_format_id = fmt['format_id']
            break
    
    if selected_format_id:
        # Download video with selected quality
        download_facebook_video(video_url, selected_format_id)
    else:
        messagebox.showerror("Error", "Selected quality format not found.")

def create_gui():
    # Creating the main window
    root = tk.Tk()
    root.title("Facebook Video Downloader")

    # Set window size
    root.geometry("500x350")

    # Label for URL input
    url_label = tk.Label(root, text="Enter Facebook Video URL:")
    url_label.pack(pady=10)

    # URL input field
    video_url_entry = tk.Entry(root, width=50)
    video_url_entry.pack(pady=5)

    # Label for quality selection
    quality_label = tk.Label(root, text="Select Video Quality:")
    quality_label.pack(pady=10)

    # Combobox for quality selection
    quality_combobox = ttk.Combobox(root, width=50)
    quality_combobox.pack(pady=5)

    # Button to fetch available formats
    fetch_quality_button = tk.Button(root, text="Fetch Available Qualities", command=lambda: choose_video_quality(get_video_formats(video_url_entry.get()), quality_combobox))
    fetch_quality_button.pack(pady=10)

    # Button to start download
    download_button = tk.Button(root, text="Download Video", command=lambda: on_download_button_click(video_url_entry, quality_combobox))
    download_button.pack(pady=10)

    # Start the GUI loop
    root.mainloop()

if __name__ == "__main__":
    create_gui()

