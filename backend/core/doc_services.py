import json
import os

from django.contrib.messages import SUCCESS
from django.core.exceptions import ValidationError
from django.http import JsonResponse

from .models import MedicalInsurance, Parent, Document
from datetime import datetime

from backend import settings


def parse_date(date_str, date_name):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'message': f"Не удалось распознать поле \'{date_name}\'"}, status=400)

def clear_exist_medical_insurance(_session_id):
    existing_insurances = MedicalInsurance.objects.filter(session_id=_session_id)
    if existing_insurances.exists():
        # Удаление связанных объектов Parent
        for insurance in existing_insurances:
            if insurance.father:
                insurance.father.delete()
            if insurance.mother:
                insurance.mother.delete()
        # Удаление объектов MedicalInsurance
        existing_insurances.delete()

def delete_garbage_file(id):
    doc = Document.objects.get(id=id)
    if doc.path:
        file_path = doc.path.path
        if os.path.exists(file_path):
            os.remove(file_path)


    doc.delete()



class DataInspector:
    def __init__(self, json_data):
        self.json_data = json_data

    def check_marriage_certificate(self, _session_id):
        try:
            data = json.loads(self.json_data)

            # Извлечение данных из JSON
            file_name = data.get('Название документа')
            if(file_name != "СВИДЕТЕЛЬСТВО О ЗАКЛЮЧЕНИИ БРАКА" and file_name != "СВИДЕТЕЛЬСТВО О БРАКЕ"):
                return JsonResponse({'message': "Загружен неверный файл"}, status=400)

            father_name = data.get('ФИО мужа')
            mother_name = data.get('ФИО жены')

            try:
                medical_insurance = MedicalInsurance.objects.get(session_id=_session_id)
            except Exception:
                return JsonResponse(
                    {'message': "Документ 'Свидетельство о рождении' не найден. Пожалуйста, следуйте инструкции"}, status=400)

            father = medical_insurance.father
            mother =medical_insurance.mother

            if(father_name != father.name):
                return JsonResponse({'message': "Неверно указаны ФИО отца"}, status=400)
            elif(mother_name != mother.name):
                return JsonResponse({'message': "Неверно указаны ФИО матери"}, status=400)

            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except json.JSONDecodeError:
            raise ValueError("Invalid JSON data")
        except ValidationError as e:
            raise ValueError(f"Validation error: {e}")

    def check_statement(self, _session_id):
        try:
            data = json.loads(self.json_data)

            # Извлечение данных из JSON
            file_name = data.get('Название документа')
            if(file_name != "Заявление"):
                return JsonResponse({'message': "Загружен неверный файл"}, status=400)

            signature = data.get('Подпись')
            date = parse_date(data.get('Дата'),'Дата')
            if isinstance(date, JsonResponse): return date

            applicant_name = data.get('ФИО заявителя')
            kid_name = data.get('ФИО ребенка')

            kid_birth = parse_date(data.get('Дата рождения ребенка'),'Дата рождения ребенка')
            if isinstance(kid_birth, JsonResponse): return kid_birth

            try:
                medical_insurance = MedicalInsurance.objects.get(session_id=_session_id)
            except Exception:
                return JsonResponse(
                    {'message': "Документ 'Свидетельство о рождении' не найден. Пожалуйста, следуйте инструкции"},status=400)

            if(not signature):
                return JsonResponse({'message': 'Подпись не распознана'}, status=400)
            elif(kid_name != medical_insurance.child_name):
                return JsonResponse({'message': 'Неверно указаны ФИО ребенка'}, status=400)
            elif (kid_birth != medical_insurance.child_birth_date):
                return JsonResponse({'message': 'Неверно указана дата рождения ребенка'}, status=400)
            elif (applicant_name == medical_insurance.father.name):
                medical_insurance.father.is_applicant = True
                medical_insurance.father.save()
                return JsonResponse({'message': 'SUCCESS'}, status=200)
            elif (applicant_name == medical_insurance.mother.name):
                medical_insurance.mother.is_applicant = True
                medical_insurance.mother.save()
                return JsonResponse({'message': 'SUCCESS'}, status=200)
            else:
                return JsonResponse({'message': 'Неверно указаны ФИО заявителя'}, status=400)





        except json.JSONDecodeError:
            raise ValueError("Invalid JSON data")
        except ValidationError as e:
            raise ValueError(f"Validation error: {e}")


    def check_birth_certificate(self, _session_id):
        try:
            data = json.loads(self.json_data)
            # Извлечение данных из JSON
            file_name = data.get('Название документа')
            if(file_name != "СВИДЕТЕЛЬСТВО О РОЖДЕНИИ"):
                return JsonResponse({'message': "Загружен неверный файл"}, status=400)

            father_name = data.get('ФИО отца')
            mother_name = data.get('ФИО матери')
            child_name = data.get('ФИО ребенка')
            child_birth_date = data.get('ДР ребенка')

            # Преобразование даты рождения ребенка в формат YYYY-MM-DD
            if child_birth_date:
                child_birth_date = datetime.strptime(child_birth_date, '%d/%m/%Y').strftime('%Y-%m-%d')

            clear_exist_medical_insurance(_session_id)


            father = Parent(
                name = father_name,
                role =Parent.FATHER,
                is_payer = False,
                is_applicant = False
            )
            mother = Parent(
                name= mother_name,
                role=Parent.MOTHER,
                is_payer=False,
                is_applicant=False
            )

            # Создание экземпляра модели
            medical_insurance = MedicalInsurance(
                session_id = _session_id,
                father=father,
                mother=mother,
                child_name=child_name,
                child_birth_date=child_birth_date,
                # Другие поля могут быть заполнены по умолчанию или оставлены пустыми
                contract_period_start=None,
                contract_period_end=None,
                total_treatment_cost=None,
                policy_number=None,
                medical_organization_data=None
            )

            # Валидация и сохранение модели
            #medical_insurance.full_clean()
            father.save()
            mother.save()

            medical_insurance.save()
            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except json.JSONDecodeError:
            raise ValueError("Invalid JSON data")
        except ValidationError as e:
            raise ValueError(f"Validation error: {e}")


