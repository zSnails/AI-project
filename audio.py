import whisper
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile

# === CONFIGURACIÓN ===
DURACION = 10  # duración de la grabación en segundos
MUESTREO = 16000  # frecuencia de muestreo (Hz)
MODELO = "base"  # tiny, base, small, medium, large

print("🎤 Grabando... habla ahora:")
audio = sd.rec(int(DURACION * MUESTREO), samplerate=MUESTREO, channels=1, dtype='float32')
sd.wait()
print("✅ Grabación finalizada")

# Guardar audio temporalmente
temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
write(temp_wav.name, MUESTREO, audio)

# Cargar modelo Whisper
print("🧠 Cargando modelo Whisper...")
model = whisper.load_model(MODELO)

# Transcribir audio
print("🗣️ Transcribiendo...")
result = model.transcribe(temp_wav.name, language="es")

print("\n📝 Texto reconocido:")
print(result["text"])
