import requests
import uuid
import json
from fpdf import FPDF
from PIL import Image
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat

rquid = str(uuid.uuid4()) # Нужен для работы всех функций
auth_token = 'YWUxNTAwNmItZWZmYi00NmNiLTk5ZjgtOTE4YWRiYWM0ZDZkOjYyOGVhNTliLWY0MmQtNGEzNS1hNDUwLWY4YzBlMjQ5NTliNg==' # Кину отдельно, чтобы его в .env добавить 
img_path = input() # Здесь должна быть функция получения изображения с фронта

prompts = {'double_page': 'Получи информацию о ФИО налогоплательщика, дате его рождения, название организации, ИНН или паспортные данные, сумму расходов, ФИО выдавшего справку, ФИО ребёнка, дату рождения ребёнка, а также наличие подписи и даты. Вывод оформи в json-формате'}

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

""" Обработка чеков (переписано)"""
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

""" Обработка свидетельства о рождении (переписано)"""
def get_birth_info(access_token, img_id):

  url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

  payload = json.dumps({
    "model": "GigaChat-Max",
    "messages": [
      {
        "role": "user",
        # "content": "Достань из этого файла ФИО ребёнка, ФИО матери, ФИО отца и дату рождения. Ответ предоставь в json формате с полями Название документа, ФИО ребёнка, ФИО отца, ФИО матери, ДР ребёнка",
        "content" : "Получи только эту информацию из файла: Название документа, ФИО ребёнка, ФИО отца, ФИО матери, Дата рождения",
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

""" Обработка свидетельства о браке (переписано)"""
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
""" Обработка справок об операции (переписано)"""
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

""" Обработка страхового полиса (переписано)"""
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
          content="Ты вадидатор данных, который получает информацию и образует json-файл по полям на выходе. Даты переводи в формат dd/mm/yyyy Выведи только следующие поля: Название документа, ФИО ребёнка, ФИО отца, ФИО матери, Дата рождения"
    )
  ] 

  messages.append(HumanMessage(content=user_content))
  res = model.invoke(messages)
  messages.append(res)
  return json.loads(res.content)

""" Обработка заявления (переписано)"""
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

def process_birth_certificate(access_token, img_id):
    """
    Функция для обработки свидетельства о рождении:
    1. Извлекает текст с изображения.
    2. Преобразует текст в JSON на основе заданного промпта.
    """
    base_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }


    prompt = """
    Прочитай предоставленный текст из свидетельства о рождении и преобразуй его в формат JSON с полями:
    - "Название документа" — фиксированное значение: "СВИДЕТЕЛЬСТВО О РОЖДЕНИИ".
    - "ФИО ребенка" — Фамилия, Имя, Отчество ребенка.
    - "ДР ребенка" — дата рождения ребенка в формате DD/MM/YYYY.
    - "ФИО отца" — Фамилия, Имя, Отчество отца.
    - "ФИО матери" — Фамилия, Имя, Отчество матери.
        НЕМНОГО ИСПОЛЬЗУЙ ЛОГИКУ, В СЛУЧАЕ ЕСЛИ ФАМИЛИИ ОТЛИЧАЮТСЯ НА ОДНУ БУКВУ ВАЛИДИРУЙ КАК ТЫ БУДЕШЬ ЧТО БЫЛО И ТД
    Убедись, что данные корректны. Игнорируй информацию о месте рождения, национальности, гражданстве и других дополнительных данных. Пример результата:
    {
      "Название документа": "СВИДЕТЕЛЬСТВО О РОЖДЕНИИ",
      "ФИО ребенка": "Иванов Иван Иванович",
      "ДР ребенка": "15/05/2010",
      "ФИО отца": "Иванов Петр Сергеевич",
      "ФИО матери": "Иванова Мария Васильевна"
    }

    В ответ дай только JSON который я запрашиваю
    """
    
    # Шаг 1: Извлечение текста с изображения
    extract_text_payload = json.dumps({
        "model": "GigaChat-Max",
        "messages": [
            {
                "role": "user",
                "content": """Выведи информацию со снимка текстом всю, сделай это качественно /
                Свидетельство о рождении на стандартном бланке. Верхняя часть документа содержит заголовок. Указаны следующие поля: ФИО ребенка, дата рождения (прописью и цифрами), место рождения, гражданство, сведения об отце (ФИО, гражданство, национальность), сведения о матери (ФИО, гражданство, национальность), орган ЗАГС, дата составления записи, дата выдачи документа, подпись и печать. В документе используются зелёные декоративные элементы, печать синяя.""",
                "attachments": [img_id]
            }
        ],
        "stream": False,
        "update_interval": 0
    })

    extract_response = requests.post(base_url, headers=headers, data=extract_text_payload, verify=False)
    if extract_response.status_code != 200:
        delete_img(access_token, img_id)
        return {"error": f"Ошибка извлечения текста: {extract_response.status_code}", "details": extract_response.text}

    extracted_text = extract_response.json()['choices'][0]['message']['content']
    # print("Извлечённый текст:")
    # print(extracted_text)

    # Шаг 2: Преобразование текста в JSON
    process_payload = json.dumps({
        "model": "GigaChat-Max",
        "messages": [
            {
                "role": "user",
                "content": f"{prompt}\n\nТекст документа:\n{extracted_text}"
            }
        ],
        "stream": False,
        "update_interval": 0
    })

    process_response = requests.post(base_url, headers=headers, data=process_payload, verify=False)
    delete_img(access_token, img_id)  # Удаляем изображение после обработки
    if process_response.status_code == 200:
        try:
            raw_content = process_response.json()['choices'][0]['message']['content']
            json_start = raw_content.find("{")
            json_end = raw_content.rfind("}") + 1
            if json_start != -1 and json_end != -1:
                cleaned_json = raw_content[json_start:json_end]
                return json.loads(cleaned_json)
            else:
                return {"error": "JSON не найден в ответе", "response": raw_content}
        except Exception as e:
            return {"error": f"Ошибка обработки JSON: {str(e)}", "response": process_response.json()}
    else:
        return {"error": f"Ошибка запроса на преобразование: {process_response.status_code}", "details": process_response.text}

def process_marriage_certificate(access_token, img_id):
    """
    Функция для обработки свидетельства о браке:
    1. Извлекает текст с изображения.
    2. Преобразует текст в JSON на основе заданного промпта.
    """
    base_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }


    prompt = """
    Прочитай предоставленный текст из свидетельства о браке и преобразуй его в формат JSON с полями:
    - "Название документа" — фиксированное значение: "СВИДЕТЕЛЬСТВО О БРАКЕ".
    - "ФИО мужа" — Фамилия, Имя, Отчество мужа.
    - "ФИО жены" — Фамилия, Имя, Отчество жены.
        НЕМНОГО ИСПОЛЬЗУЙ ЛОГИКУ, В СЛУЧАЕ ЕСЛИ ФАМИЛИИ ОТЛИЧАЮТСЯ НА ОДНУ БУКВУ ВАЛИДИРУЙ КАК ТЫ БУДЕШЬ ЧТО БЫЛО И ТД
    Убедись, что данные корректны. Игнорируй информацию о месте рождения, национальности, гражданстве и других дополнительных данных. Пример результата:
    {
      "Название документа": "СВИДЕТЕЛЬСТВО О БРАКЕ",
      "ФИО мужа": "Иванов Петр Сергеевич",
      "ФИО жены": "Иванова Мария Васильевна"
    }

    В ответ дай только JSON который я запрашиваю
    """
    
    # Шаг 1: Извлечение текста с изображения
    extract_text_payload = json.dumps({
        "model": "GigaChat-Max",
        "messages": [
            {
                "role": "user",
                "content": """Выведи информацию со снимка текстом всю, сделай это качественно /
                Свидетельство о браке на стандартном бланке. Верхняя часть документа содержит заголовок. Указаны следующие поля: информация про мужа (ФИО и Дата рождения),  информация про жену (ФИО и Дата рождения), дата заключения брака и дата оформления брака (прописью и цифрами), присвоенные фамилии, место регистрации, дата выдачи, подпись и печать. В документе используются красные декоративные элементы, печать синяя.""",
                "attachments": [img_id]
            }
        ],
        "stream": False,
        "update_interval": 0
    })

    extract_response = requests.post(base_url, headers=headers, data=extract_text_payload, verify=False)
    if extract_response.status_code != 200:
        delete_img(access_token, img_id)
        return {"error": f"Ошибка извлечения текста: {extract_response.status_code}", "details": extract_response.text}

    extracted_text = extract_response.json()['choices'][0]['message']['content']
    # print("Извлечённый текст:")
    # print(extracted_text)

    # Шаг 2: Преобразование текста в JSON
    process_payload = json.dumps({
        "model": "GigaChat-Max",
        "messages": [
            {
                "role": "user",
                "content": f"{prompt}\n\nТекст документа:\n{extracted_text}"
            }
        ],
        "stream": False,
        "update_interval": 0
    })

    process_response = requests.post(base_url, headers=headers, data=process_payload, verify=False)
    delete_img(access_token, img_id)  # Удаляем изображение после обработки
    if process_response.status_code == 200:
        try:
            raw_content = process_response.json()['choices'][0]['message']['content']
            json_start = raw_content.find("{")
            json_end = raw_content.rfind("}") + 1
            if json_start != -1 and json_end != -1:
                cleaned_json = raw_content[json_start:json_end]
                return json.loads(cleaned_json)
            else:
                return {"error": "JSON не найден в ответе", "response": raw_content}
        except Exception as e:
            return {"error": f"Ошибка обработки JSON: {str(e)}", "response": process_response.json()}
    else:
        return {"error": f"Ошибка запроса на преобразование: {process_response.status_code}", "details": process_response.text}

def process_statement(access_token, img_id):
    """
    Функция для обработки заявления:
    1. Извлекает текст с изображения.
    2. Преобразует текст в JSON на основе заданного промпта.
    """
    base_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }


    prompt = """
    Прочитай предоставленный текст из свидетельства о рождении и преобразуй его в формат JSON с полями:
    - "Название документа" — фиксированное значение: "ЗАЯВЛЕНИЕ НА МЕД. ОБСЛУЖИВАНИЕ".
    - "ФИО ребенка" — Фамилия, Имя, Отчество ребенка.
    - "ДР ребенка" — дата рождения ребенка в формате DD/MM/YYYY.
    - "Дата подписания" — дата оформления заявления в формате DD/MM/YYYY.
    - "Подпись" — Наличие подписи в формате true/false.
        НЕМНОГО ИСПОЛЬЗУЙ ЛОГИКУ, В СЛУЧАЕ ЕСЛИ ФАМИЛИИ ОТЛИЧАЮТСЯ НА ОДНУ БУКВУ ВАЛИДИРУЙ КАК ТЫ БУДЕШЬ ЧТО БЫЛО И ТД
    Убедись, что данные корректны. Игнорируй информацию о месте рождения, национальности, гражданстве и других дополнительных данных. Пример результата:
    {
      "Название документа": "ЗАЯВЛЕНИЕ НА МЕД. ОБСЛУЖИВАНИЕ",
      "ФИО ребенка": "Иванов Иван Иванович",
      "ДР ребенка": "15/05/2010",
      "Дата подписания": "26/11/2024",
      "Подпись": True
    }

    В ответ дай только JSON который я запрашиваю
    """
    
    # Шаг 1: Извлечение текста с изображения
    extract_text_payload = json.dumps({
        "model": "GigaChat-Max",
        "messages": [
            {
                "role": "user",
                "content": """Выведи информацию со снимка текстом всю, сделай это качественно /
                Заявление на мед. обсулживание на стандартном бланке. Верхняя часть документа содержит заголовок. Там же оформлено обращение по полям с ФИО руководителя, ФИО заместителя и ФИО заявителя, текст самого заявления, в конце находится поле для даты подписания и место для подписи.""",
                "attachments": [img_id]
            }
        ],
        "stream": False,
        "update_interval": 0
    })

    extract_response = requests.post(base_url, headers=headers, data=extract_text_payload, verify=False)
    if extract_response.status_code != 200:
        delete_img(access_token, img_id)
        return {"error": f"Ошибка извлечения текста: {extract_response.status_code}", "details": extract_response.text}

    extracted_text = extract_response.json()['choices'][0]['message']['content']
    # print("Извлечённый текст:")
    # print(extracted_text)

    # Шаг 2: Преобразование текста в JSON
    process_payload = json.dumps({
        "model": "GigaChat-Max",
        "messages": [
            {
                "role": "user",
                "content": f"{prompt}\n\nТекст документа:\n{extracted_text}"
            }
        ],
        "stream": False,
        "update_interval": 0
    })

    process_response = requests.post(base_url, headers=headers, data=process_payload, verify=False)
    delete_img(access_token, img_id)  # Удаляем изображение после обработки
    if process_response.status_code == 200:
        try:
            raw_content = process_response.json()['choices'][0]['message']['content']
            json_start = raw_content.find("{")
            json_end = raw_content.rfind("}") + 1
            if json_start != -1 and json_end != -1:
                cleaned_json = raw_content[json_start:json_end]
                return json.loads(cleaned_json)
            else:
                return {"error": "JSON не найден в ответе", "response": raw_content}
        except Exception as e:
            return {"error": f"Ошибка обработки JSON: {str(e)}", "response": process_response.json()}
    else:
        return {"error": f"Ошибка запроса на преобразование: {process_response.status_code}", "details": process_response.text}

def process_reciept(access_token, img_id):
    """
    Функция для обработки чеков:
    1. Извлекает текст с изображения.
    2. Преобразует текст в JSON на основе заданного промпта.
    """
    base_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }


    prompt = """
    Прочитай предоставленный текст из чека и преобразуй его в формат JSON с полями:
    - "Способ оплаты" — Способ оплаты наличиными или безналично".
    - "ФИО плательщика" — Фамилия, Имя, Отчество плательщика.
    - "Дата оплаты" — дата оплаты в формате DD/MM/YYYY.
    - "Сумма" — Итоговая сумма по операции.
    - "Место оплаты" — Название организации, где была проведена оплата.
    - "Подпись" — Наличие подписи в формате true/false.
    - "Печать" — Наличие печати в формате true/false.
        НЕМНОГО ИСПОЛЬЗУЙ ЛОГИКУ, В СЛУЧАЕ ЕСЛИ ФАМИЛИИ ОТЛИЧАЮТСЯ НА ОДНУ БУКВУ ВАЛИДИРУЙ КАК ТЫ БУДЕШЬ ЧТО БЫЛО И ТД
    Убедись, что данные корректны. Игнорируй информацию о месте рождения, национальности, гражданстве и других дополнительных данных. Пример результата:
    {
      "Способ оплаты": "Безналично",
      "ФИО плательщика": "Иванов Иван Иванович",
      "Дата оплаты": "15/05/2024",
      "Сумма": "16000.00",
      "Место оплаты": "Больница",
      "Подпись": True,
      "Печать": True
    }

    В ответ дай только JSON который я запрашиваю
    """
    
    # Шаг 1: Извлечение текста с изображения
    extract_text_payload = json.dumps({
        "model": "GigaChat-Max",
        "messages": [
            {
                "role": "user",
                "content": """Выведи информацию со снимка текстом всю, сделай это качественно /
                Стандартный чек, сверху находится шапка с названием места оплаты, далее идут пункты по которым была произведена оплата, количество и цена. В конце указана итоговая стоимость, способ оплаты, дата оплаты, подпись и печать. Печать синяя.""",
                "attachments": [img_id]
            }
        ],
        "stream": False,
        "update_interval": 0
    })

    extract_response = requests.post(base_url, headers=headers, data=extract_text_payload, verify=False)
    if extract_response.status_code != 200:
        delete_img(access_token, img_id)
        return {"error": f"Ошибка извлечения текста: {extract_response.status_code}", "details": extract_response.text}

    extracted_text = extract_response.json()['choices'][0]['message']['content']
    # print("Извлечённый текст:")
    # print(extracted_text)

    # Шаг 2: Преобразование текста в JSON
    process_payload = json.dumps({
        "model": "GigaChat-Max",
        "messages": [
            {
                "role": "user",
                "content": f"{prompt}\n\nТекст документа:\n{extracted_text}"
            }
        ],
        "stream": False,
        "update_interval": 0
    })

    process_response = requests.post(base_url, headers=headers, data=process_payload, verify=False)
    delete_img(access_token, img_id)  # Удаляем изображение после обработки
    if process_response.status_code == 200:
        try:
            raw_content = process_response.json()['choices'][0]['message']['content']
            json_start = raw_content.find("{")
            json_end = raw_content.rfind("}") + 1
            if json_start != -1 and json_end != -1:
                cleaned_json = raw_content[json_start:json_end]
                return json.loads(cleaned_json)
            else:
                return {"error": "JSON не найден в ответе", "response": raw_content}
        except Exception as e:
            return {"error": f"Ошибка обработки JSON: {str(e)}", "response": process_response.json()}
    else:
        return {"error": f"Ошибка запроса на преобразование: {process_response.status_code}", "details": process_response.text}

def process_reference(access_token, img_id):
    """
    Функция для обработки справок по чекам:
    1. Извлекает текст с изображения.
    2. Преобразует текст в JSON на основе заданного промпта.
    """
    base_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }


    prompt = """
    Прочитай предоставленный текст из чека и преобразуй его в формат JSON с полями:
    - "ФИО плательщика" — Фамилия, Имя, Отчество плательщика.
    - "Дата оплаты" — дата оплаты в формате DD/MM/YYYY.
    - "Сумма" — Итоговая сумма по операции.
    - "Место оплаты" — Название организации, где была проведена оплата.
        НЕМНОГО ИСПОЛЬЗУЙ ЛОГИКУ, В СЛУЧАЕ ЕСЛИ ФАМИЛИИ ОТЛИЧАЮТСЯ НА ОДНУ БУКВУ ВАЛИДИРУЙ КАК ТЫ БУДЕШЬ ЧТО БЫЛО И ТД
    Убедись, что данные корректны. Игнорируй информацию о месте рождения, национальности, гражданстве и других дополнительных данных. Пример результата:
    {
      "ФИО плательщика": "Иванов Иван Иванович",
      "Дата оплаты": "15/05/2024",
      "Сумма": "16000.00",
      "Место оплаты": "Больница",
    }

    В ответ дай только JSON который я запрашиваю
    """
    
    # Шаг 1: Извлечение текста с изображения
    extract_text_payload = json.dumps({
        "model": "GigaChat-Max",
        "messages": [
            {
                "role": "user",
                "content": """Выведи информацию со снимка текстом всю, сделай это качественно /
                Стандартный чек, сверху находится шапка с названием банка, который был использован для оплаты. В центре указаны сумма оплаты, ФИО плательщика,дата оплаты, место оплаты, номера счетов. В документе могут быть декоративные элементы разного цвета.""",
                "attachments": [img_id]
            }
        ],
        "stream": False,
        "update_interval": 0
    })

    extract_response = requests.post(base_url, headers=headers, data=extract_text_payload, verify=False)
    if extract_response.status_code != 200:
        delete_img(access_token, img_id)
        return {"error": f"Ошибка извлечения текста: {extract_response.status_code}", "details": extract_response.text}

    extracted_text = extract_response.json()['choices'][0]['message']['content']
    # print("Извлечённый текст:")
    # print(extracted_text)

    # Шаг 2: Преобразование текста в JSON
    process_payload = json.dumps({
        "model": "GigaChat-Max",
        "messages": [
            {
                "role": "user",
                "content": f"{prompt}\n\nТекст документа:\n{extracted_text}"
            }
        ],
        "stream": False,
        "update_interval": 0
    })

    process_response = requests.post(base_url, headers=headers, data=process_payload, verify=False)
    delete_img(access_token, img_id)  # Удаляем изображение после обработки
    if process_response.status_code == 200:
        try:
            raw_content = process_response.json()['choices'][0]['message']['content']
            json_start = raw_content.find("{")
            json_end = raw_content.rfind("}") + 1
            if json_start != -1 and json_end != -1:
                cleaned_json = raw_content[json_start:json_end]
                return json.loads(cleaned_json)
            else:
                return {"error": "JSON не найден в ответе", "response": raw_content}
        except Exception as e:
            return {"error": f"Ошибка обработки JSON: {str(e)}", "response": process_response.json()}
    else:
        return {"error": f"Ошибка запроса на преобразование: {process_response.status_code}", "details": process_response.text}

def process_insurance(access_token, img_id):
    """
    Функция для обработки полиса ДМС:
    1. Извлекает текст с изображения.
    2. Преобразует текст в JSON на основе заданного промпта.
    """
    base_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }


    prompt = """
    Прочитай предоставленный текст из чека и преобразуй его в формат JSON с полями:
    - "ФИО ребенка" — Фамилия, Имя, Отчество ребенка.
    - "ДР ребенка" — дата рождения ребенка в формате DD/MM/YYYY.
    - "Номер полиса" — Уникальный номер полиса.
    - "Срок действия" — Дата, до которой действителен ДМС в формате DD/MM/YYYY.
        НЕМНОГО ИСПОЛЬЗУЙ ЛОГИКУ, В СЛУЧАЕ ЕСЛИ ФАМИЛИИ ОТЛИЧАЮТСЯ НА ОДНУ БУКВУ ВАЛИДИРУЙ КАК ТЫ БУДЕШЬ ЧТО БЫЛО И ТД
    Убедись, что данные корректны. Игнорируй информацию о месте рождения, национальности, гражданстве и других дополнительных данных. Пример результата:
    {
      "ФИО ребенка": "Иванов Иван Иванович",
      "ДР ребенка": "15/05/2010",
      "Номер полиса": "4400 2888 9654 3821",
      "Срок действия": "Больница",
    }

    В ответ дай только JSON который я запрашиваю
    """
    
    # Шаг 1: Извлечение текста с изображения
    extract_text_payload = json.dumps({
        "model": "GigaChat-Max",
        "messages": [
            {
                "role": "user",
                "content": """Выведи информацию со снимка текстом всю, сделай это качественно /
                Стандартный полис ДМС содержит шапку с названием фирмы Страховщика, далее идёт блок с информацией страховщика (Адрес, Реквизиты, Контактные данные), блок с информацией страхователя (ФИО, адрес, паспорт, телефон, реквизиты, гражданство), блок с информацией застрахованного (ФИО, адрес, паспорт, телефон, гражданство), варианты страхования, срок действия полиса, подпись и печать. Документ содержит декоративные элементы разных цветов, печать синего цвета.""",
                "attachments": [img_id]
            }
        ],
        "stream": False,
        "update_interval": 0
    })

    extract_response = requests.post(base_url, headers=headers, data=extract_text_payload, verify=False)
    if extract_response.status_code != 200:
        delete_img(access_token, img_id)
        return {"error": f"Ошибка извлечения текста: {extract_response.status_code}", "details": extract_response.text}

    extracted_text = extract_response.json()['choices'][0]['message']['content']
    # print("Извлечённый текст:")
    # print(extracted_text)

    # Шаг 2: Преобразование текста в JSON
    process_payload = json.dumps({
        "model": "GigaChat-Max",
        "messages": [
            {
                "role": "user",
                "content": f"{prompt}\n\nТекст документа:\n{extracted_text}"
            }
        ],
        "stream": False,
        "update_interval": 0
    })

    process_response = requests.post(base_url, headers=headers, data=process_payload, verify=False)
    delete_img(access_token, img_id)  # Удаляем изображение после обработки
    if process_response.status_code == 200:
        try:
            raw_content = process_response.json()['choices'][0]['message']['content']
            json_start = raw_content.find("{")
            json_end = raw_content.rfind("}") + 1
            if json_start != -1 and json_end != -1:
                cleaned_json = raw_content[json_start:json_end]
                return json.loads(cleaned_json)
            else:
                return {"error": "JSON не найден в ответе", "response": raw_content}
        except Exception as e:
            return {"error": f"Ошибка обработки JSON: {str(e)}", "response": process_response.json()}
    else:
        return {"error": f"Ошибка запроса на преобразование: {process_response.status_code}", "details": process_response.text}

def process_franchise_reference(access_token, img_id):
    """
    Функция для обработки справки франшизы:
    1. Извлекает текст с изображения.
    2. Преобразует текст в JSON на основе заданного промпта.
    """
    base_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }


    prompt = """
    Прочитай предоставленный текст из чека и преобразуй его в формат JSON с полями:
    - "ФИО плательщика" — Фамилия, Имя, Отчество плательщика.
    - "ФИО ребенка" — Фамилия, Имя, Отчество ребенка.
    - "ДР ребенка" — дата рождения ребенка в формате DD/MM/YYYY.
    - "Номер полиса" — Уникальный номер полиса.
    - "Срок действия страхования" — Дата, до которой действительно страхование в формате DD/MM/YYYY.
        НЕМНОГО ИСПОЛЬЗУЙ ЛОГИКУ, В СЛУЧАЕ ЕСЛИ ФАМИЛИИ ОТЛИЧАЮТСЯ НА ОДНУ БУКВУ ВАЛИДИРУЙ КАК ТЫ БУДЕШЬ ЧТО БЫЛО И ТД
    Убедись, что данные корректны. Игнорируй информацию о месте рождения, национальности, гражданстве и других дополнительных данных. Пример результата:
    {
      "ФИО ребенка": "Иванов Иван Иванович",
      "ДР ребенка": "15/05/2010",
      "Номер полиса": "4400 2888 9654 3821",
      "Срок действия": "Больница",
    }

    В ответ дай только JSON который я запрашиваю
    """
    
    # Шаг 1: Извлечение текста с изображения
    extract_text_payload = json.dumps({
        "model": "GigaChat-Max",
        "messages": [
            {
                "role": "user",
                "content": """Выведи информацию со снимка текстом всю, сделай это качественно /
                В справке находится информации о человеке оплатившем страхование ребенка, информация о застрахованном ребенке, информация из полиса ДМС (срок действия, номер полиса), срок дейтсвия страховки""",
                "attachments": [img_id]
            }
        ],
        "stream": False,
        "update_interval": 0
    })

    extract_response = requests.post(base_url, headers=headers, data=extract_text_payload, verify=False)
    if extract_response.status_code != 200:
        delete_img(access_token, img_id)
        return {"error": f"Ошибка извлечения текста: {extract_response.status_code}", "details": extract_response.text}

    extracted_text = extract_response.json()['choices'][0]['message']['content']
    # print("Извлечённый текст:")
    # print(extracted_text)

    # Шаг 2: Преобразование текста в JSON
    process_payload = json.dumps({
        "model": "GigaChat-Max",
        "messages": [
            {
                "role": "user",
                "content": f"{prompt}\n\nТекст документа:\n{extracted_text}"
            }
        ],
        "stream": False,
        "update_interval": 0
    })

    process_response = requests.post(base_url, headers=headers, data=process_payload, verify=False)
    delete_img(access_token, img_id)  # Удаляем изображение после обработки
    if process_response.status_code == 200:
        try:
            raw_content = process_response.json()['choices'][0]['message']['content']
            json_start = raw_content.find("{")
            json_end = raw_content.rfind("}") + 1
            if json_start != -1 and json_end != -1:
                cleaned_json = raw_content[json_start:json_end]
                return json.loads(cleaned_json)
            else:
                return {"error": "JSON не найден в ответе", "response": raw_content}
        except Exception as e:
            return {"error": f"Ошибка обработки JSON: {str(e)}", "response": process_response.json()}
    else:
        return {"error": f"Ошибка запроса на преобразование: {process_response.status_code}", "details": process_response.text}

