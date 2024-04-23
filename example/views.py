# example/views.py

from openai import OpenAI
from django.shortcuts import render
from django.http import JsonResponse
import os


def rot13_encrypt(input_string):
    result = ''
    for char in input_string:
        char_code = ord(char)

        if 65 <= char_code <= 90:
            result += chr(((char_code - 65 + 13) % 26) + 65)
        elif 97 <= char_code <= 122:
            result += chr(((char_code - 97 + 13) % 26) + 97)
        else:
            result += char

    return result


# openai.api_key = os.environ.get('api_key')
# OpenAI.api_key = rot13_encrypt("fx-tRkZ4auwLoAPzS2huTMmG3OyoxSWdcCOwYOIg8o1qwTuncJq")

client = OpenAI(
    # This is the default and can be omitted
    api_key=rot13_encrypt("fx-xadnsgv624qHRbs5u4nrG3OyoxSW5bnQzqYDMMDg0SdV81K4"),
)

def index(request):
    return render(request, 'index.html')

import requests



def save_audio(request):

    hasura_url = "https://registergeerd.hasura.app/api/rest/getPrompt/1"

    headers = {
        "Content-Type": "application/json",
        "x-hasura-admin-secret":
        "i5po5Bap0VZ9YjcuQ0vzxAy7LBzI0XbuvILake89SEqFsQf2S6ok67BaihIeT7wb",  # Replace with your Hasura admin secret
    }

    response = requests.get(hasura_url, headers=headers)
    # print(response)
    
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")


    
    if request.method == 'POST':
        text = request.POST.get('text')

        # audio_file = request.FILES['audio_file']
        # print(audio_file)
        # audio_byte = audio_file.read()
        
        # transcript = client.audio.transcriptions.create(
        #     model="whisper-1", 
        #     file=audio_byte
        # )

        # system_msg = " here are two transcript of the user, look at the one that makes sense more and do what it asks and JUST ANSWER DIRECTLY"
        system_msg = data["prompt"][0]["prompt"]
        token = data["prompt"][0]["token"]
        temp = data["prompt"][0]["temp"]
       
        user_msg = "first transcript: " + text #+ "; second transcript: " + transcript.text
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature = temp,
        max_tokens = token,
        messages=[{"role": "system", "content": system_msg},
                        {"role": "user", "content": user_msg}]
        )
        
        response2 = response.choices[0]

        response3 = response2.message

        response4 = response3.content

        return JsonResponse({'id': response4})
    return JsonResponse({'error': 'Invalid request method'})


def admin(request):
    return render(request, 'admin.html')



# example/views.py

from openai import OpenAI
from django.shortcuts import render
from django.http import JsonResponse
import os
import base64
import os

# def encode_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode('utf-8')

def rot13_encrypt2(input_string):
    result = ''
    for char in input_string:
        char_code = ord(char)

        if 65 <= char_code <= 90:
            result += chr(((char_code - 65 + 13) % 26) + 65)
        elif 97 <= char_code <= 122:
            result += chr(((char_code - 97 + 13) % 26) + 97)
        else:
            result += char

    return result


os.environ["OPENAI_API_KEY"] = rot13_encrypt2("fx-cebw-YBlVcFEOf92bDUbcQATmG3OyoxSWTNJh8mm11FPdrYA9V3zU")

def api_gpt4(request):
    # image_local = './image.png'
    
    if request.method == 'POST':
        base64_image = request.POST.get('base64_image')
        prompt = request.POST.get('prompt')
    
        # image_url = f"data:image/jpeg;base64,{encode_image(base64_image)}"

        client = OpenAI()

        try:
            response = client.chat.completions.create(
                model='gpt-4-vision-preview',
                messages=[
                    {
                        "role": "assistant",
                        "content": [
                            {
                                "type": "text", 
                                "text": prompt
                            },
                            {
                                "type": "image_url", 
                                "image_url": {
                                    "url": base64_image
                                }
                            }
                        ],
                    }
                ],
                max_tokens=500,
            )
        except Exception as e:
            return JsonResponse({'error': 'Error gpt4 ' + e}, status=400)
        response2 = response.choices[0]
        response3 = response2.message
        response4 = response3.content
        
        return JsonResponse({'answer': response4})
    
    return JsonResponse({'error': 'Fuck you '}, status=69)