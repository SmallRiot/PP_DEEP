import requests
import uuid
import json
from fpdf import FPDF
from PIL import Image
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat

rquid = str(uuid.uuid4()) # Нужен для работы всех функций
auth_token = '' # Кину отдельно, чтобы его в .env добавить 
# img_path = input() # Здесь должна быть функция получения изображения с фронта

prompts = {'double_page': 'Получи информацию о ФИО налогоплательщика, дате его рождения, название организации, ИНН или паспортные данные, сумму расходов, ФИО выдавшего справку, ФИО ребёнка, дату рождения ребёнка, а также наличие подписи и даты. Вывод оформи в json-формате',
           'franchise_reciept': 'Получи информацию о способе оплаты (True, если безнал), ФИО плателщьика, дата оплаты, сумма оплаты, место оплаты, наличие подписи и печати. Ответ оформи в json-формате с полями Способ оплаты, ФИО, Дата, Сумма, Место',
           'franchise_reference': 'Получи информацию о ФИО плательщика, дате оплаты, сумме оплаты, месте оплаты. Ответ предоставь в json-формате с полями ФИО, Дата, Сумма, Место',
           'isnurence_reference': 'Получи информацию о ФИО плательщика, ФИО ребёнка, годе рождения ребёнка, сроке действия страхования и номере полиса ДМС. Ответ предоставь в json-формате с полями ФИО плательщика, ФИО ребёнка, Год рождения, Срок, Номер',
           'statement': 'Получи информацию о дате, ФИО заявителя и ФИО ребёнка, а также наличие подписи (true/false). Выведи информацию в json-формате с полями Название документа, Дата, Подпись, ФИО заявителя, ФИО ребёнка'}

""" Токен должен быть один для всех и обновляться раз в 30 минут """
def get_access_token(rquid, auth_token):
  url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

  payload='scope=GIGACHAT_API_PERS'

  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
    'RqUID': rquid,
    'Authorization': 'Basic ' + auth_token
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)

  if response.status_code == 200:
    return response.json()['access_token']
  else:
    return response.status_code

# Получение токена для работы остальных функций
access_token = get_access_token(rquid, auth_token)

""" Это функция загрузки изобржения в API. 
Когда изображение приходит с фронта, сначала нужно добавить его в API, а потом получить id """
def load_img(access_token, img_path):
  url = "https://gigachat.devices.sberbank.ru/api/v1/files"

  payload = {'purpose': 'general'}

  files=[
  ('file',('file',open(str(img_path),'rb'),'image/png'))
  ]

  headers = {
  'Authorization': 'Bearer ' + access_token
  }

  response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False)

  if response.status_code == 200:
    return response.json()['id']
  else:
    return response.status_code

def load_pdf(access_token, img_path):
  url = "https://gigachat.devices.sberbank.ru/api/v1/files"

  payload = {'purpose': 'general'}

  files=[
  ('file',('file',open(str(img_path),'rb'),'application/pdf'))
  ]

  headers = {
  'Authorization': 'Bearer ' + access_token
  }

  response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False)

  if response.status_code == 200:
    return response.json()['id']
  else:
    return response

""" Для того, чтобы не хранить персональные данные и не перегружать API, все изоюбражения удаляются после обработки """
def delete_img(access_token, img_id):
  url = "https://gigachat.devices.sberbank.ru/api/v1/files/:" + img_id + "/delete"

  payload={}

  headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer ' + access_token
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)

  if response.status_code == 200:
    return response.json()
  else:
    return response.status_code

""" Обработка чеков """
def get_reciept_info(access_token, img_id):

  url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

  payload = json.dumps({
    "model": "GigaChat-Pro",
    "messages": [
      {
        "role": "user",
        "content": "Получи информацию о названии компании, дате совершения операции в формате dd.mm.yy, способе оплате (Наличными/Безналичными) и итоговой стоимости и ответ представь в json-формате с полями: Название компании, Дата операции, Итоговая сумма, Способ оплаты. В ответе укажи только json",
        "attachments": [
          img_id
        ]
      }
    ],
    "stream": False,
    "update_interval": 0
  })

  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + access_token
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)
  delete_img(access_token, img_id)

  if response.status_code == 200:
    return response.json()['choices'][0]['message']['content']
  else:
    return response.status_code

""" Обработка свидетельства о рождении """
def get_birth_info(access_token, img_id):

  url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

  payload = json.dumps({
    "model": "GigaChat-Max",
    "messages": [
      {
        "role": "user",
        # "content": "Достань из этого файла ФИО ребёнка, ФИО матери, ФИО отца и дату рождения. Ответ предоставь в json формате с полями Название документа, ФИО ребёнка, ФИО отца, ФИО матери, ДР ребёнка",
        "сontent" : "Получи только эту информацию из файла: Название документа, ФИО ребёнка, ФИО отца, ФИО матери, Дата рождения",
        "attachments": [
          img_id
        ]
      }
    ],
    "stream": False,
    "update_interval": 0
  })

  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + access_token
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)
  delete_img(access_token, img_id)

  if response.status_code == 200:
    return response.json()['choices'][0]['message']['content']
  else:
    return response.status_code

""" Обработка свидетельства о браке """
def get_marriage_info(access_token, img_id):

  url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

  payload = json.dumps({
    "model": "GigaChat-Max",
    "messages": [
      {
        "role": "user",
        # "content": "Достань из изображения информацию о названии документа, ФИО мужа и ФИО жены и ответ представь в json-формате с полями: Название документа, ФИО мужа, ФИО жены. В ответе укажи только json",
        "content" : "Расскажи, что находится в этом файле",
        "attachments": [
          img_id
        ]
      }
    ],
    "stream": False,
    "update_interval": 0
  })

  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + access_token
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)
  delete_img(access_token, img_id)

  if response.status_code == 200:
    return response.json()['choices'][0]['message']['content']
  else:
    return response.status_code

# print(get_marriage_info(access_token, load_img(access_token, img_path)))
""" Обработка справок об операции """
def get_reference_info(access_token, img_id):

  url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

  payload = json.dumps({
    "model": "GigaChat-Pro",
    "messages": [
      {
        "role": "user",
        "content": "Получи информацию о дате совершения операции в формате dd.mm.yy, ФИО держателя карты и итоговой стоимости и ответ представь в json-формате с полями: Дата операции, Итоговая сумма, ФИО. В ответе укажи только json",
        "attachments": [
          img_id
        ]
      }
    ],
    "stream": False,
    "update_interval": 0
  })

  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + access_token
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)
  delete_img(access_token, img_id)

  if response.status_code == 200:
    return response.json()['choices'][0]['message']['content']
  else:
    return response.status_code

""" Обработка договора об оказании услуг """
def get_contract_info(access_token, img_id):

  url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

  payload = json.dumps({
    "model": "GigaChat-Pro",
    "messages": [
      {
        "role": "user",
        "content": "Получи информацию о данных мед-организации и наличие подписи и печати (В ответе подпись и печать указать как True, если есть) и ответ представь в json-формате с полями: Мед-организация, Подпись, Печать. В ответе укажи только json",
        "attachments": [
          img_id
        ]
      }
    ],
    "stream": False,
    "update_interval": 0
  })

  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + access_token
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)
  delete_img(access_token, img_id)

  if response.status_code == 200:
    return response.json()['choices'][0]['message']['content']
  else:
    return response.status_code

""" Обработка страхового полиса """
def get_insurance_info(access_token, img_id):

  url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

  payload = json.dumps({
    "model": "GigaChat-Pro",
    "messages": [
      {
        "role": "user",
        "content": "Получи информацию о ФИО ребёнка, Дате рождения ребёнка, Номере полиса и сроке действия (формат всех дат dd.mm.yyyy) и ответ представь в json-формате с полями: ФИО, Дата рождения, Номер полиса, Срок действия. В ответе укажи только json",
        "attachments": [
          img_id
        ]
      }
    ],
    "stream": False,
    "update_interval": 0
  })

  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + access_token
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)
  delete_img(access_token, img_id)

  if response.status_code == 200:
    return response.json()['choices'][0]['message']['content']
  else:
    return response.status_code

def get_info(access_token, img_id, prompt):
  
  url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

  payload = json.dumps({
    "model": "GigaChat-Pro",
    "messages": [
      {
        "role": "user",
        "content": prompt,
        "attachments": [
          img_id
        ]
      }
    ],
    "stream": False,
    "update_interval": 0
  })

  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + access_token
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)
  delete_img(access_token, img_id)

  if response.status_code == 200:
    return response.json()['choices'][0]['message']['content']
  else:
    return response.status_code

def images_to_pdf(image_paths, output_pdf_path):

    pdf = FPDF()

    for image_path in image_paths:
        with Image.open(image_path) as img:
            width, height = img.size

        pdf.add_page()

        pdf_width = 210
        pdf_height = 297

        if width > height:
            scale_factor = pdf_width / width
            img_width = pdf_width
            img_height = height * scale_factor
        else:
            scale_factor = pdf_height / height
            img_width = width * scale_factor
            img_height = pdf_height

        pdf.image(image_path, x=0, y=0, w=img_width, h=img_height)

    pdf.output(output_pdf_path)

def sup_response(user_content, auth_token):

  model = GigaChat(
      credentials=auth_token,
      scope="GIGACHAT_API_PERS",
      model="GigaChat",
      verify_ssl_certs=False,
  )

  messages = [
      SystemMessage(
          content="Ты вадидатор данных, который получает информацию и образует json-файл по полям на выходе. На каждый полученный текст верни json, где все поля находтся на одном уровне. Даты приводи в формат dd/mm/yyyy. Если в документе встречается ФИО, записывай каждое ФИО в отдельное поле с соотвествующим наименованием"
    )
  ] 

  messages.append(HumanMessage(content=user_content))
  res = model.invoke(messages)
  messages.append(res)
  return json.loads(res.content)

def get_statement_info(access_token, img_id):
  
  url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

  payload = json.dumps({
    "model": "GigaChat-Pro",
    "messages": [
      {
        "role": "user",
        "content": "Получи информацию о дате, ФИО заявителя и ФИО ребёнка, а также наличие подписи (true/false). Выведи информацию в json-формате с полями Название документа, Дата, Подпись, ФИО заявителя, ФИО ребёнка",
        "attachments": [
          img_id
        ]
      }
    ],
    "stream": False,
    "update_interval": 0
  })

  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + access_token
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)
  delete_img(access_token, img_id)

  if response.status_code == 200:
    return response.json()['choices'][0]['message']['content']
  else:
    return response.status_code
