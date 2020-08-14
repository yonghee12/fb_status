import requests
def send_line_msg(message, token='zYp6BSEjISJii2GsKB259EbwowIxZvGYlMk0HtQEa7U'):
    TARGET_URL = 'https://notify-api.line.me/api/notify'
    response = requests.post(
      TARGET_URL,
      headers={
        'Authorization': 'Bearer ' + token
      },
      data={
        'message': message
      }
    )
    return response.text