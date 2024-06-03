import openai
import azure.cognitiveservices.speech as speechsdk
deployment_name = "test-gpt-jay"
openai.api_type = "azure"
openai.api_key ="d65ae29b824e4b9e84000f40150fae59"
openai.api_base = "https://test-azureopenai-jay.openai.azure.com/"
openai.api_version = "2024-02-01"
AZURE_SPEECH_KEY="412a1362f5d742dc94d224092b1914e2"
AZURE_SPEECH_REGION="eastus"
speechconfig = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY,region=AZURE_SPEECH_REGION)
speechconfig.speech_recognition_language="en-US"
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speechconfig, audio_config=audio_config)
print("You can speak now. I am listening!.....")
speech_recognizer_result = speech_recognizer.recognize_once_async().get()
output = speech_recognizer_result.text
print(output)
prompt =output
result = openai.Completion.create(
    prompt=prompt,
    temperature=0,
    max_tokens=300,
    deployment_id=deployment_name
)
print(result.choices[0].text.strip(" \n"))
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speechconfig, audio_config=audio_config)
speech_synthesis_result = speech_synthesizer.speak_text_async(result.choices[0].text.strip(" \n")).get()

