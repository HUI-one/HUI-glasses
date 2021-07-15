import os
import time

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import subprocess

from google.cloud import speech
#from google.cloud.speech import speech
#from google.cloud.speech import speech

from micstream import MicrophoneStream

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
"static-manifest-001030-7fb9047e9fd7.json"
#======================================display
i2c = busio.I2C(SCL, SDA)

disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

disp.fill(0)
disp.show()


width = disp.width
height = disp.height
font_m12 = ImageFont.truetype('/home/pi/disp_oled/NanumMyeongjo.ttf', 12)
font_m13 = ImageFont.truetype('/home/pi/disp_oled/NanumMyeongjo.ttf', 13)
font_mm = ImageFont.truetype('/home/pi/disp_oled/Minecraftia-Regular.ttf', 13)
image = Image.new('1',(width,height))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)
padding = 0
top = padding
bottom = height-padding
x = 0
font = ImageFont.load_default()
while True:

    # 디스플레이 초기화
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    #디스플레이 내용 (좌표) , 문자열, 폰트, ?
    draw.text((x, top), "음성인식을 시작합니다.",  font=font_m13, fill=255)
 
    # Display 띄우기.
    disp.image(image)
    disp.show()
    time.sleep(.1)
    break
#=====================display init_end
def situation():
     os.system("arecord --duration=4 ~/record/filename.wav")
#=====================google_speech
# Audio recording parameters
#RATE =44100 
RATE =16000
CHUNK =int(RATE /10)  # 100ms

#print stt 20*5 character
def listen_print_loop(responses): 

    for response in responses:
        situation()
        result = response.results[0]
        transcript = result.alternatives[0].transcript
        str_1 = str(transcript)
        str_2 = str_3 = str_4 = ""
        str_5 = "상황표현"
# -----------------------------
        if len(str_1) >= 15 :
            str_2 = str_1[14:28]
            str_3 = str_1[29:43]
            str_4 = str_1[44:58]
            str_1 = str_1[0:13]
# -----------------------------
        print(str_1, ", ", str_2, ", ", str_3)

        draw.rectangle((0,0,128,48), outline=0, fill=0)
        draw.text((x,top), str_1, font=font_m12, fill=255)
        draw.text((x,top+12), str_2, font=font_m12, fill=255)
        draw.text((x,top+24), str_3, font=font_m12, fill=255)
        draw.text((x,top+35), str_4, font=font_m12, fill=255)

        draw.rectangle((0,48,128,68), outline=0, fill=0)
        draw.text((x,top+48), str_5, font=font_m12, fill=255)
        disp.image(image)
        disp.show()
        time.sleep(.1)
        if u'quit'in transcript or u'stop'in transcript:
            print('quit..')
            break

language_code ='ko-KR'  # a BCP-47 language tag

client = speech.SpeechClient()
config = speech.RecognitionConfig(
	encoding =speech.RecognitionConfig.AudioEncoding.LINEAR16,
	sample_rate_hertz =RATE,
	language_code =language_code)
streaming_config = speech.StreamingRecognitionConfig(config =config)

with MicrophoneStream(RATE, CHUNK) as stream:
	audio_generator = stream.generator()
	requests = (speech.StreamingRecognizeRequest(audio_content =content)
				for content in audio_generator)
	responses = client.streaming_recognize(streaming_config, requests)
	
	listen_print_loop(responses)