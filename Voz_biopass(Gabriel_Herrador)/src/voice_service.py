import speech_recognition as sr
import sounddevice as sd
import numpy as np
import io
import wave
import time

class VoiceService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.sample_rate = 16000 # Estándar para reconocimiento de voz

    def listen_and_recognize(self):
        """
        Captura el audio usando sounddevice y lo traduce a texto.
        """
        start_time = time.time()
        duration = 5  # Segundos a grabar
        
        try:
            print(f"Escuchando durante {duration} segundos...")
            # Grabar audio
            audio_data = sd.rec(int(duration * self.sample_rate), samplerate=self.sample_rate, channels=1, dtype='int16')
            sd.wait()  # Esperar a que termine la grabación
            
            end_time = time.time()
            latencia = round(end_time - start_time, 2)
            
            # Convertir el array de numpy a un objeto AudioData de SpeechRecognition
            # Primero lo pasamos por un buffer de memoria como si fuera un archivo WAV
            with io.BytesIO() as wav_buffer:
                with wave.open(wav_buffer, 'wb') as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2) # 16-bit
                    wf.setframerate(self.sample_rate)
                    wf.writeframes(audio_data.tobytes())
                
                wav_buffer.seek(0)
                with sr.AudioFile(wav_buffer) as source:
                    audio = self.recognizer.record(source)
            
            # Reconocimiento
            result = self.recognizer.recognize_google(audio, language="es-ES", show_all=True)
            
            if not result or 'alternative' not in result:
                return None, 0, latencia, "No se reconoció ninguna frase."
            
            best_alt = result['alternative'][0]
            texto = best_alt.get('transcript')
            confianza = best_alt.get('confidence', 0.0)
            
            return texto, confianza, latencia, None

        except Exception as e:
            return None, 0, 0, f"Error capturando audio: {e}"
