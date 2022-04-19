from aip import AipSpeech

APP_ID = '25984923'
API_KEY = 'cwucKGfTZeN8CkOmlRU0z2pE'
SECRET_KEY = 'MCFIfiXHLWTaHbshizEwPtxcN7E00Utj'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

def listen():
    with open('recording.wav', 'rb') as f:
        audio_data = f.read()

    result = client.asr(audio_data, 'wav', 16000, {
        'dev_pid': 1536,
    })

    result_text = result["result"][0]

    print("you said: " + result_text)

    return result_text

listen()
