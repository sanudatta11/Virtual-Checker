import json

 
def speak(data):
    data = '"'+data+'"'
    os.system('google_speech -l en ' + data + ' -e speed 1 overdrive 9 echo 0.5 0.8 3 0.3')
import pyowm
from watson_developer_cloud import ConversationV1
import pyaudio
import wave
import os
import json
from os.path import join, dirname
from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud import AlchemyLanguageV1 as AlchemyLanguage
owm = pyowm.OWM('cafe11a1aa017272eed13ef4d7e25061')
 
conversation = ConversationV1(
  username='14ba30d2-0b1d-4752-84a1-59a81dcbc9bb',
  password='OK7tPRng5UGf',
  version='2017-02-03'
)
 
#getting weather condition
def get_weather():
  observation = owm.weather_at_place('Chennai,India,in')
  w = observation.get_weather()
                              # <Weather - reference time=2013-12-18 09:20,
                              # status=Clouds>`+
 
  # Weather details
  w.get_wind()                  # {'speed': 4.6, 'deg': 330}
  w.get_humidity()              # 87
  w.get_temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
  array=json.dumps(w.get_temperature('celsius'));
  a=json.loads(array);
  return a;
 
#Getting Voice System
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 800
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"
 
audio = pyaudio.PyAudio()
 
# start Recording
stream = audio.open(format=FORMAT, channels=1,
                rate=48000, input=True,
                frames_per_buffer=CHUNK)
print("recording...")
frames = []
 
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print("finished recording")
 
 
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
 
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()
 
 
def transcribe_audio():
    username = "10a52f77-c7d4-4f86-85bd-8aa1fa0a60ac"
    path_to_audio_file = "file.wav"
    password = "dWlVi2nmLc1Q"
    speech_to_text = SpeechToTextV1(username='10a52f77-c7d4-4f86-85bd-8aa1fa0a60ac',password="dWlVi2nmLc1Q")
    with open(path_to_audio_file,"rb") as audio_file:
        return(speech_to_text.recognize(audio_file,content_type="audio/wav"))
 
 
#getting data from the audio
input_text=transcribe_audio();
print(input_text);
input_text=input_text['results'][0]['alternatives'][0]['transcript']
a=get_weather();
context = {};
context['weather_speed']=a["temp_max"];
workspace_id = 'cabf44ea-edd2-4a08-8eac-f5aeb8a778e1'
response = conversation.message(
  workspace_id=workspace_id,
   context=context,
  message_input={'text': input_text}
)
my_output=json.dumps(response['output']['text'][0])
print(my_output[1:-1]);
 
data_speak = my_output[1:-1]
speak(data_speak)
