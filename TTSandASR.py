from openai import OpenAI
from pathlib import Path


def transcribe_audio_file(file_path: str):
    """
    使用 OpenAI Whisper API 对指定音频文件进行转录。
    
    :param file_path: 音频文件的绝对路径或相对路径
    :return: Whisper API 返回的转录结果对象
    """
    client = OpenAI(api_key="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")
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcription

# ASR测试代码
# transcription = transcribe_audio_file("sft_3.wav")
# print(transcription.text)

def generate_audio_files(audio_content:str):
    client = OpenAI(api_key="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")
    speech_file_path = Path(__file__).parent / "sft_0.wav"
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=audio_content,
    )
    response.stream_to_file(speech_file_path)
    return 1  # 只生成一个音频文件，因此返回1

# TTS测试代码
# generate_audio_files("""
#                      Hello this is kexin. I am a master’s student at SUSTech School of Design, majoring in Industrial Design Engineering. I am also a member of the aiStudio. My research field is human-computer interaction, and I am currently exploring the use of AI to support education and learning. A large language model is used to support learning in the area of teachers' pedagogical gestures. Specifically, we designed a novice teacher, Novobo, who was given specific teaching scenarios and language to work with. Novobo would generate gesture descriptions based on them and give the theory behind her gestures, and the teachers could comment on Novobo's gestures and teach Novobo their own interpretations through words or actions. Through the joint discussion and practice of gestures, embodied knowledge is expressed and transferred between teachers.
#                      """)


