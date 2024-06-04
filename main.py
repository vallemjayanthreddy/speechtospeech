import openai
import datetime  # Import datetime for timestamps
import azure.cognitiveservices.speech as speechsdk
import logging

deployment_name = "test-gpt-jay"
openai.api_type = "azure"
openai.api_key ="mykey"
openai.api_base = "https://test-azureopenai-jay.openai.azure.com/"
openai.api_version = "2024-02-01"

AZURE_SPEECH_KEY="mykey"
AZURE_SPEECH_REGION="eastus"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

speechconfig = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY,region=AZURE_SPEECH_REGION)
speechconfig.speech_recognition_language="en-US"
speech_recognition_start_time= datetime.datetime.now()
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speechconfig, audio_config=audio_config)
logging.info("Listening for speech...")  # Added logging for speech recognition start
print("You can speak now. I am listening!.....")
speech_recognizer_result = speech_recognizer.recognize_once_async().get()
speech_recognition_end_time = datetime.datetime.now()  # Capture end time
logging.info(f"Speech recognition completed in {(speech_recognition_end_time - speech_recognition_start_time).total_seconds()} seconds")

output = speech_recognizer_result.text
print(output)
prompt =output
logging.info("Calling OpenAI API...")  # Added logging for OpenAI call start
openai_call_start_time = datetime.datetime.now()
result = openai.Completion.create(
    prompt=prompt,
    temperature=0,
    max_tokens=300,
    deployment_id=deployment_name
)
openai_call_end_time = datetime.datetime.now()  # Capture end time
logging.info(f"OpenAI API call completed in {(openai_call_end_time - openai_call_start_time).total_seconds()} seconds")
# Log completion time
print(result.choices[0].text.strip(" \n"))
logging.info("Synthesizing speech...")
# Added logging for text-to-speech start
speech_synthesis_start_time = datetime.datetime.now()
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speechconfig, audio_config=audio_config)
speech_synthesis_result = speech_synthesizer.speak_text_async(result.choices[0].text.strip(" \n")).get()
speech_synthesis_end_time = datetime.datetime.now()  # Capture end time
logging.info(f"Speech synthesis completed in {(speech_synthesis_end_time - speech_synthesis_start_time).total_seconds()} seconds")
# Log completion time
