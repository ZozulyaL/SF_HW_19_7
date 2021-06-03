
import pytest
from api import PetFriends
from settings import valid_email, valid_password
from settings import no_valid_email, no_valid_password
import os

pf = PetFriends()

def test_get_api_key_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=' '):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter='my_pets')
    print(result)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Кошкин', animal_type='кот',
                                     age='8', pet_photo='images/8rlCnGn4tgA.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/IMG_0401.JPG")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

                 #HOMEWORK 19 UNIT

#HW Test 1
def test_get_api_key_no_valid_user(email=no_valid_email, password=no_valid_password):
    """ Проверяем что запрос api ключа c невалидным данными пользователя не возвращает 200 и key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status != 200
    assert 'key' is not result

#HW-Test 2
def test_get_list_of_pets_with_invalid_key(filter=''):
    """Проверка получение списка питомцев с неправильным ключом"""
    auth_key = {'key': '8abc63282685111bf29417f23bcbaae44d110cef017199919bfe90gf'}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status != 200
    assert 'pets' not in result

#HW-Test 3
def test_add_new_pet_with_symbol_in_name(name="??|||//", animal_type="косуля",
                                          age="3", pet_photo="images/8rlCnGn4tgA.jpg"):
    """Проверка на создание питомца со специальными символами в имени"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

#HW-Test 4
def test_add_new_pet_with_invalid_age(name="Кузик", animal_type="такса",
                                       age="а", pet_photo="images/8rlCnGn4tgA.jpg"):
    """Проверка создания питомца с str в графе 'age'"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
   # assert status != 503
    assert 'age' in result

#HW-Test 5
def test_add_new_pet_without_photo_valid_data(name="Kuzzik", animal_type="tvar", age="67"):
    """Проверка создания питомца без фотографии с корректными данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

#HW-Test 6
def test_add_new_pet_without_photo_invalid_key(name="Kuzzik", animal_type="tvar", age="67"):
    """Проверка создания питомца без фотографии с некорректным ключом"""
    auth_key = {'key': '8abc63282685111bf29417f23bcbaae44d110cef017199919bfe90gf'}
    status, result = pf.add_new_pet_without_photo(auth_key,name,animal_type,age)

    assert status != 200
    assert 'name' not in result

#HW-Test 7
def test_add_new_pet_without_photo_invalid_age(name="Счастье", animal_type="tvar", age="аппроолллллллrfvbnnmkkjyttresxccbnnmmkjytrdsxwazxc"
                                                                                       "ппппппппппппппппппппппппппппппппvbnm,.llhjjjjjjjjjjjjjgfddssss"):
    """Проверка отсутствия строкового ограничения в поле age"""
    _, auth_key = pf.get_api_key(valid_email,valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert 'age'  in result

#HW-Test 8
def test_add_correct_photo_to_pet(pet_photo="images/IMG_0401.JPG"):
    """Проверка добавление фотографии к питомцу"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    pet_id = my_pets['pets'][-1]['id']
    status, result = pf.add_photo_for_pet(auth_key,pet_id,pet_photo)

    assert status == 200
    assert 'jpg' or 'png' in 'pet_photo'

# HW-Test 9
def test_add_incorrect_photo_to_pet(pet_photo="images/fignya.gif"):
    """Проверка добавления не корректного формата фотографии к питомцу"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    pet_id = my_pets['pets'][-1]['id']
    status, result = pf.add_photo_for_pet(auth_key,pet_id,pet_photo)

    assert status != 200
    assert status == 503
    assert 'jpg' or 'png' not in 'pet_photo'

# HW-Test 10
def test_delete_with_incorrect_id_pet():
    """Проверка удаления питомца с некорректным ID"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key)
    my_pets['pets'][-1]['id'] = '8abc63282685111bf29417f23bcaae44d110cef017199919bfe90gf'

    if len(my_pets['pets']) > 0:
        status, result = pf.delete_pet(auth_key, my_pets['pets'][-1]['id'])
        assert status == 200
    else:
        raise Exception("There's no my pets")
