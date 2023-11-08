from PyPDF4.pdf import PdfFileReader
import pyttsx3
from speech_recognition import Recognizer, AudioFile
from pydub import AudioSegment
import os

def pdf_to_audio(pdf_file, page):
    try:
        reader = PdfFileReader(open(pdf_file, 'rb'))
        engine = pyttsx3.init()
        page_number = int(page) - 1  # Convert to 0-based page number

        if page_number >= 0 and page_number < reader.getNumPages():
            text = reader.getPage(page_number).extractText()
            engine.say(text)
            engine.runAndWait()
        else:
            print("Invalid page number. Please provide a valid page number.")
    except Exception as e:
        print(f"Error: {e}")

def audio_to_text(audio_file, output_file):
    try:
        audio_file_extension = os.path.splitext(audio_file)[1]

        if audio_file_extension not in ['.wav', '.mp3']:
            print("Invalid audio file format. Supported formats are .wav and .mp3.")
            return

        if audio_file_extension == '.mp3':
            audio_file_name = os.path.splitext(os.path.basename(audio_file))[0]
            audio_file = AudioSegment.from_file(audio_file, format='mp3')
            audio_file.export(f'{audio_file_name}.wav', format='wav')
            audio_file = f'{audio_file_name}.wav'

        r = Recognizer()
        with AudioFile(audio_file) as source:
            r.pause_threshold = 5
            speech = r.record(source)
            text = r.recognize_google(speech)
            with open(output_file, 'w') as text_file:
                text_file.write(text)
        print("Text extracted from audio and saved to the specified file.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    option = input("Choose an option:\n1. Convert PDF to Audio\n2. Convert Audio to Text\n")

    if option == '1':
        pdf_file = input("Enter the PDF file location (with extension): ")
        page = input("Enter the page number to read from the PDF: ")
        pdf_to_audio(pdf_file, page)
    elif option == '2':
        audio_file = input("Enter the audio file location (in .wav or .mp3 format): ")
        output_file = input("Enter the output text file location: ")
        audio_to_text(audio_file, output_file)
    else:
        print("Invalid option. Please select 1 or 2.")
