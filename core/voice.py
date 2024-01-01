from gtts import gTTS
import tempfile
import threading
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"  # Hide pygame's welcome message, remind me to remove this later, they deserve recognize, thank you for the fast tts
import pygame
import tkinter as tk

# Initialize Pygame's mixer
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
volume = 0.25
subtitles = True

class TransparentSubtitlesWindow:
    def __init__(self, text):
        self.root = tk.Tk()
        self.text = text
        self.label = tk.Label(self.root, text=self.text, font=('Helvetica', 16), fg='white', bg='black')
        self.label.pack()

        # Set the window to be always on top, transparent, and without decorations
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-transparentcolor', 'black')

        # Set window position
        self.root.geometry('+%d+%d' % (self.root.winfo_screenwidth() // 2 - self.label.winfo_reqwidth() // 2,
                                       self.root.winfo_screenheight() - 100))
        self.update()

    def update(self):
        self.label.configure(text=self.text)
        self.root.update_idletasks()
        self.root.update()

    def change_text(self, new_text, duration):
        self.text = new_text
        self.update()

        # Schedule removing the text after the duration
        self.root.after(duration, lambda: self.label.configure(text=""))

    def close(self):
        self.root.quit()  # changed from destroy() to quit()


def calculate_duration_of_speech(text, lang='en', wpm=150):
    """Estimate the duration the subtitles should be displayed based on words per minute (WPM)"""
    words = text.split()
    word_count = len(words)
    duration_in_seconds = (word_count / wpm) * 60
    return int(duration_in_seconds * 1000)  # Convert to milliseconds for tkinter's after method


def play_audio(file_path, text, lang='en'):
    # Estimate the duration the subtitles should be shown
    duration = calculate_duration_of_speech(text, lang)

    # Load and play audio file
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()

    # When the audio finishes, stop the mixer and remove the temporary file
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove(file_path)


def set_volume(volume_level):
    global volume
    volume = volume_level
    pygame.mixer.music.set_volume(volume)

def set_subtitles(subtitles_bool):
    global subtitles
    subtitles = subtitles_bool


def speaker(text, lang='en'):
    # Initialize all of pygame's modules
    pygame.init()

    # Temporary mp3 file creation
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
        tts = gTTS(text=text, lang=lang)
        tts.save(fp.name)
        temp_file_path = fp.name

    # Start the subtitles thread
    if subtitles is True:
        def setup_subtitles():
            window = TransparentSubtitlesWindow(text)
            window.change_text(text, calculate_duration_of_speech(text, lang))
            window.root.mainloop()

        subtitles_thread = threading.Thread(target=setup_subtitles)
        subtitles_thread.daemon = True  # Now the thread will close when the main program exits
        subtitles_thread.start()
    else:
        subtitles_thread = None

    # Start the audio thread
    audio_thread = threading.Thread(target=play_audio, args=(temp_file_path, text, lang))
    audio_thread.daemon = True
    audio_thread.start()

    # Return the threads in case the caller wants to track them
    return audio_thread, subtitles_thread


if __name__ == '__main__':
    text_to_speak = "Hello, this is a test."
    speaker(text_to_speak)
    # Main script can do other tasks here, threads will not prevent script from exiting