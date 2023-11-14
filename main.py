import google.cloud.texttospeech as tts
from google.cloud import translate
import os

log = os.path.join("translate.log")

def text_to_wav(voice_name: str, text: str):
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input,
        voice=voice_params,
        audio_config=audio_config,
    )

    filename = f"{voice_name}.wav"
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Generated speech saved to "{filename}"')

def translate_text(text="Hello, world!", project_id="alien-clover-405022"):
    translated = ""
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": "pt-BR",
            "target_language_code": "en-US",
        }
    )

    for translation in response.translations:
        translated = translation.translated_text
    if (os.path.exists(log)):
        arquivo = open(log, 'r')
        conteudo = arquivo.readlines()
        conteudo.append(translated)

        arquivo = open(log, 'w')
        arquivo.writelines(conteudo)

        arquivo.close()

    else:
        arquivo = open(log, 'a')
        arquivo.write(translated)
        arquivo.close()
    return translated

def traduzECriaAudio(project_id, text):
    txtTransl = translate_text(text, project_id)
    text_to_wav("pt-BR-Neural2-A", text)
    text_to_wav("en-US-Studio-O", txtTransl)

project_id = "inserir o codigo do projeto do google"
text = "inserir o texto em portugues"
traduzECriaAudio(project_id, text)
