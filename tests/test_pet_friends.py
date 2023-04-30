from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Марсик', animal_type='сибирский',
                                     age='4', pet_photo='../images/1cat.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo)

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
        pf.add_new_pet_with_photo(auth_key, "Суперкот", "кот", "3", "../images/1cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Марсюша', animal_type='Сибирский', age=1):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

# Отсюда начинаются мои тесты

def test_add_new_pet_without_photo_with_valid_data(name='Персик', animal_type='рэгдолл',
                                     age='4'):
    """Проверяем что можно добавить питомца без фото с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_without_photo_with_invalid_age(name='Стасик', animal_type='рэгдолл',
                                     age='999999999999999999999999999999999999999999999'):
    """Проверяем что нельзя добавить питомца без фото с некорректными данными возраста"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status != 200
    assert result['name'] == name

def test_add_new_pet_without_photo_with_invalid_data(name='', animal_type='',
                                     age=''):
    """Проверяем что нельзя добавить питомца без фото с некорректными (пустыми) данными возраста"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status != 200
    assert result['name'] == name


def test_successful_add_pet_photo(pet_photo='../images/1cat.jpg'):
    """Проверяем возможность загрузки фото питомца к существующему питомцу без фото"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового без фото и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, "Новыйкот", "кот", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и загружаем фото
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.add_pet_photo(auth_key, pet_id, pet_photo)

    assert status == 200


def test_successful_upd_pet_photo(pet_photo='../images/2cat.jpg'):
    """Проверяем возможность обновления фото питомца у существующего питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_with_photo(auth_key, "Новыйкот", "кот", "3", "../images/1cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и загружаем фото
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.add_pet_photo(auth_key, pet_id, pet_photo)

    assert status == 200


def test_negative_add_pet_photo_with_incorrect_pet_id(pet_photo='../images/1cat.jpg', pet_id='123'):
    """Проверяем невозможность загрузки фото питомца к несуществующему питомцу"""

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Загружаем фото по несуществующему id питомца
    pet_id = pet_id
    status, _ = pf.add_pet_photo(auth_key, pet_id, pet_photo)
    # Убеждаемся,что сервер не загрузил фото к несуществующему питомцу
    assert status == 500


def test_get_all_pets_with_invalid_key(filter='а'):
    """ Проверяем что запрос питомцев по несуществующему фильтру не производится """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status != 200
    #assert len(result['pets']) == 0


def test_get_all_pets_with_invalid_filter(filter='а'):
    """ Проверяем что запрос питомцев по несуществующему фильтру не производится """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status != 200


def test_get_all_pets_with_invalid_key(filter=''):
    """ Проверяем что запрос всех питомцев, без авторизации пользователя, не возвращает список питомцев."""

    auth_key = {'auth_key': 0}
    try:
        result = pf.get_list_of_pets(auth_key, filter)
    except KeyError:
        result = 'KeyError'
        print()
    assert result == 'KeyError'

def test_authorization_with_invalid_password(email=valid_email, password='123'):
    """ Проверяем что запрос api ключа c неверным паролем или email возвращает статус 403"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403

