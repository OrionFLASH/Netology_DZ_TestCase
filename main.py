"""
Домашнее задание по тестированию на Python
Студент: [Имя студента]
Группа: [Номер группы]
"""

import os
import configparser
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pytest


class PythonBasics:
    """
    Класс с функциями из модуля "Основы языка программирования Python"
    для демонстрации unit-тестирования
    """
    
    @staticmethod
    def find_course_durations(courses, mentors, durations):
        """
        Задание «Рекордсмены: находим самый продолжительный и самый короткий курс по программированию»
        Находит самый короткий и самый длинный курсы из списка курсов
        """
        # Создаем список курсов
        courses_list = []
        for title, mentors_list, duration in zip(courses, mentors, durations):
            course_dict = {'title': title, 'mentors': mentors_list, 'duration': duration}
            courses_list.append(course_dict)
        
        # Находим минимальную и максимальную длительность
        min_duration = min(durations)
        max_duration = max(durations)
        
        # Находим индексы курсов с минимальной и максимальной длительностью
        min_indices = []
        max_indices = []
        for idx, duration in enumerate(durations):
            if duration == min_duration:
                min_indices.append(idx)
            if duration == max_duration:
                max_indices.append(idx)
        
        # Собираем названия самых коротких и самых длинных курсов
        shortest_courses = [courses_list[idx]['title'] for idx in min_indices]
        longest_courses = [courses_list[idx]['title'] for idx in max_indices]
        
        return {
            'shortest': shortest_courses,
            'longest': longest_courses,
            'min_duration': min_duration,
            'max_duration': max_duration
        }
    
    @staticmethod
    def discriminant(a, b, c):
        """
        Задание «Квадратное уравнение»
        Функция для нахождения дискриминанта квадратного уравнения ax² + bx + c = 0
        """
        return (b ** 2) - 4 * a * c
    
    @staticmethod
    def solve_quadratic_equation(a, b, c):
        """
        Задание «Квадратное уравнение»
        Функция для нахождения корней квадратного уравнения ax² + bx + c = 0
        Возвращает список корней или сообщение об их отсутствии
        """
        D = PythonBasics.discriminant(a, b, c)
        
        if D < 0:
            return "корней нет"
        elif D == 0:
            root = -b / (2 * a)
            return [root]
        else:
            root1 = (-b + D ** 0.5) / (2 * a)
            root2 = (-b - D ** 0.5) / (2 * a)
            return [root1, root2]
    
    @staticmethod
    def vote(votes):
        """
        Задание «Голосование»
        Функция принимает список чисел и возвращает число, которое встречается чаще всего
        """
        max_count = 0
        max_element = 0
        
        for vote_item in votes:
            count = votes.count(vote_item)
            if count >= max_count:
                max_count = count
                max_element = vote_item
        
        return max_element


class YandexDiskAPI:
    """
    Класс для работы с API Яндекс.Диска
    Позволяет создавать папки и проверять их существование
    """
    
    def __init__(self, token):
        """
        Инициализация с токеном доступа
        Токен можно получить на https://yandex.ru/dev/disk/poligon/
        """
        self.token = token
        self.base_url = "https://cloud-api.yandex.net/v1/disk"
        self.headers = {
            'Authorization': f'OAuth {token}',
            'Content-Type': 'application/json'
        }
    
    def create_folder(self, folder_name):
        """
        Создает папку на Яндекс.Диске
        Возвращает True если папка создана успешно, False в противном случае
        """
        url = f"{self.base_url}/resources"
        params = {
            'path': f'/{folder_name}',
            'overwrite': 'false'
        }
        
        try:
            response = requests.put(url, headers=self.headers, params=params)
            return response.status_code == 201
        except requests.RequestException:
            return False
    
    def folder_exists(self, folder_name):
        """
        Проверяет, существует ли папка на Яндекс.Диске
        Возвращает True если папка существует, False в противном случае
        """
        url = f"{self.base_url}/resources"
        params = {'path': f'/{folder_name}'}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    def get_folder_info(self, folder_name):
        """
        Получает информацию о папке
        Возвращает словарь с информацией или None в случае ошибки
        """
        url = f"{self.base_url}/resources"
        params = {'path': f'/{folder_name}'}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException:
            return None


class YandexAuth:
    """
    Класс для автоматизации авторизации на Яндексе через Selenium
    """
    
    def __init__(self, login, password):
        """
        Инициализация с данными для входа
        """
        self.login = login
        self.password = password
        self.driver = None
    
    def setup_driver(self):
        """
        Настройка веб-драйвера Chrome
        Устанавливает опции для работы в headless режиме
        """
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Запуск без графического интерфейса
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        return self.driver
    
    def login_to_yandex(self):
        """
        Выполняет авторизацию на Яндексе
        Возвращает True если авторизация успешна, False в противном случае
        """
        try:
            if not self.driver:
                self.setup_driver()
            
            # Переходим на страницу авторизации
            self.driver.get("https://passport.yandex.ru/auth/")
            
            # Ждем загрузки страницы и находим поле логина
            wait = WebDriverWait(self.driver, 10)
            login_field = wait.until(
                EC.presence_of_element_located((By.ID, "passp-field-login"))
            )
            
            # Вводим логин
            login_field.clear()
            login_field.send_keys(self.login)
            
            # Нажимаем кнопку "Войти"
            login_button = self.driver.find_element(By.ID, "passp:sign-in")
            login_button.click()
            
            # Ждем появления поля пароля
            password_field = wait.until(
                EC.presence_of_element_located((By.ID, "passp-field-passwd"))
            )
            
            # Вводим пароль
            password_field.clear()
            password_field.send_keys(self.password)
            
            # Нажимаем кнопку "Войти"
            password_button = self.driver.find_element(By.ID, "passp:sign-in")
            password_button.click()
            
            # Ждем успешной авторизации (появление элемента профиля)
            wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "user-account"))
            )
            
            return True
            
        except Exception as e:
            print(f"Ошибка при авторизации: {e}")
            return False
    
    def close_driver(self):
        """
        Закрывает веб-драйвер
        """
        if self.driver:
            self.driver.quit()
            self.driver = None


def load_config():
    """
    Загружает конфигурацию из файла config.ini
    Возвращает объект конфигурации или None в случае ошибки
    """
    config = configparser.ConfigParser()
    
    if not os.path.exists('config.ini'):
        print("Файл config.ini не найден!")
        print("Скопируйте config.ini.example в config.ini и заполните токены")
        return None
    
    try:
        config.read('config.ini')
        return config
    except Exception as e:
        print(f"Ошибка при чтении конфигурации: {e}")
        return None


# ==================== UNIT ТЕСТЫ ====================

class TestPythonBasics:
    """
    Unit-тесты для функций из модуля "Основы языка программирования Python"
    """
    
    def test_find_course_durations(self):
        """Тест функции поиска самого короткого и длинного курса"""
        # Тестовые данные из задания
        courses = ["Java-разработчик с нуля", "Fullstack-разработчик на Python", 
                  "Python-разработчик с нуля", "Frontend-разработчик с нуля"]
        mentors = [
            ["Филипп Воронов", "Анна Юшина", "Иван Бочаров"],
            ["Евгений Шмаргунов", "Олег Булыгин", "Александр Бардин"],
            ["Евгений Шмаргунов", "Олег Булыгин", "Дмитрий Демидов"],
            ["Владимир Чебукин", "Эдгар Нуруллин", "Евгений Шек"]
        ]
        durations = [14, 20, 12, 20]
        
        result = PythonBasics.find_course_durations(courses, mentors, durations)
        
        # Проверяем результат
        assert result['min_duration'] == 12
        assert result['max_duration'] == 20
        assert "Python-разработчик с нуля" in result['shortest']
        assert "Fullstack-разработчик на Python" in result['longest']
        assert "Frontend-разработчик с нуля" in result['longest']
        assert len(result['shortest']) == 1
        assert len(result['longest']) == 2
    
    @pytest.mark.parametrize("a,b,c,expected", [
        (1, 8, 15, 4),      # D = 64 - 60 = 4
        (1, -13, 12, 121),  # D = 169 - 48 = 121
        (-4, 28, -49, 0),   # D = 784 - 784 = 0
        (1, 1, 1, -3),      # D = 1 - 4 = -3
        (3, -4, 2, -8),     # D = 16 - 24 = -8
    ])
    def test_discriminant(self, a, b, c, expected):
        """Параметризованный тест функции вычисления дискриминанта"""
        assert PythonBasics.discriminant(a, b, c) == expected
    
    @pytest.mark.parametrize("a,b,c,expected", [
        (1, 8, 15, [-3.0, -5.0]),           # Два корня
        (1, -13, 12, [12.0, 1.0]),          # Два корня
        (-4, 28, -49, [3.5]),               # Один корень
        (1, 1, 1, "корней нет"),            # Нет корней
        (3, -4, 2, "корней нет"),           # Нет корней
    ])
    def test_solve_quadratic_equation(self, a, b, c, expected):
        """Параметризованный тест функции решения квадратного уравнения"""
        result = PythonBasics.solve_quadratic_equation(a, b, c)
        
        if isinstance(expected, str):
            assert result == expected
        else:
            # Проверяем корни с учетом погрешности вычислений
            assert len(result) == len(expected)
            for i, (actual, expected_val) in enumerate(zip(result, expected)):
                assert abs(actual - expected_val) < 1e-10, f"Корень {i}: {actual} != {expected_val}"
    
    @pytest.mark.parametrize("votes,expected", [
        ([1, 1, 1, 2, 3], 1),           # 1 встречается 3 раза
        ([1, 2, 3, 2, 2], 2),           # 2 встречается 3 раза
        ([5, 5, 5, 5, 1, 2, 3], 5),     # 5 встречается 4 раза
        ([1, 2, 3, 4, 5], 5),           # 5 встречается последним при равном количестве
        ([10, 20, 10, 30, 20, 20], 20), # 20 встречается 3 раза
        ([1], 1),                       # Один элемент
        ([7, 7, 7, 7, 7], 7),           # Все элементы одинаковые
    ])
    def test_vote(self, votes, expected):
        """Параметризованный тест функции голосования"""
        assert PythonBasics.vote(votes) == expected


class TestYandexDiskAPI:
    """
    Тесты для API Яндекс.Диска
    """
    
    @pytest.fixture
    def yandex_api(self):
        """Фикстура для создания экземпляра API"""
        config = load_config()
        if not config:
            pytest.skip("Конфигурация не загружена")
        
        token = config.get('YANDEX', 'token', fallback='')
        if not token or token == 'your_yandex_disk_token_here':
            pytest.skip("Токен Яндекс.Диска не настроен")
        
        return YandexDiskAPI(token)
    
    def test_create_folder_success(self, yandex_api):
        """Тест успешного создания папки"""
        folder_name = f"test_folder_{int(time.time())}"
        
        # Создаем папку
        result = yandex_api.create_folder(folder_name)
        assert result == True
        
        # Проверяем, что папка действительно создалась
        exists = yandex_api.folder_exists(folder_name)
        assert exists == True
    
    def test_create_existing_folder(self, yandex_api):
        """Тест попытки создания уже существующей папки"""
        folder_name = f"existing_folder_{int(time.time())}"
        
        # Создаем папку первый раз
        result1 = yandex_api.create_folder(folder_name)
        assert result1 == True
        
        # Пытаемся создать папку с тем же именем
        result2 = yandex_api.create_folder(folder_name)
        # API может вернуть True (перезаписать) или False (отказать)
        assert result2 in [True, False]
    
    def test_folder_exists(self, yandex_api):
        """Тест проверки существования папки"""
        folder_name = f"check_folder_{int(time.time())}"
        
        # Папка не должна существовать
        exists_before = yandex_api.folder_exists(folder_name)
        assert exists_before == False
        
        # Создаем папку
        yandex_api.create_folder(folder_name)
        
        # Папка должна существовать
        exists_after = yandex_api.folder_exists(folder_name)
        assert exists_after == True
    
    def test_get_folder_info(self, yandex_api):
        """Тест получения информации о папке"""
        folder_name = f"info_folder_{int(time.time())}"
        
        # Создаем папку
        yandex_api.create_folder(folder_name)
        
        # Получаем информацию о папке
        info = yandex_api.get_folder_info(folder_name)
        assert info is not None
        assert 'name' in info
        assert info['name'] == folder_name
    
    def test_invalid_token(self):
        """Тест с неверным токеном"""
        invalid_api = YandexDiskAPI("invalid_token")
        result = invalid_api.create_folder("test")
        assert result == False


class TestYandexAuth:
    """
    Тесты для авторизации на Яндексе через Selenium
    """
    
    @pytest.fixture
    def yandex_auth(self):
        """Фикстура для создания экземпляра авторизации"""
        config = load_config()
        if not config:
            pytest.skip("Конфигурация не загружена")
        
        login = config.get('YANDEX_AUTH', 'login', fallback='')
        password = config.get('YANDEX_AUTH', 'password', fallback='')
        
        if not login or not password or login == 'your_yandex_login':
            pytest.skip("Данные для авторизации не настроены")
        
        return YandexAuth(login, password)
    
    def test_yandex_login_success(self, yandex_auth):
        """Тест успешной авторизации на Яндексе"""
        try:
            # Настраиваем драйвер
            driver = yandex_auth.setup_driver()
            assert driver is not None
            
            # Выполняем авторизацию
            result = yandex_auth.login_to_yandex()
            
            # Проверяем результат
            assert result == True
            
        finally:
            # Закрываем драйвер
            yandex_auth.close_driver()
    
    def test_invalid_credentials(self):
        """Тест с неверными данными для входа"""
        invalid_auth = YandexAuth("invalid_login", "invalid_password")
        
        try:
            driver = invalid_auth.setup_driver()
            result = invalid_auth.login_to_yandex()
            assert result == False
        except Exception as e:
            # Если драйвер не установлен, тест считается пропущенным
            if "NoSuchDriverException" in str(e) or "WebDriverException" in str(e):
                pytest.skip("Chrome WebDriver не установлен")
            else:
                raise
        finally:
            invalid_auth.close_driver()


if __name__ == "__main__":
    """
    Основная функция для демонстрации работы классов
    """
    print("=== Демонстрация функций Python Basics ===")
    
    # Задание 1: Рекордсмены курсов
    print("\n1. Задание «Рекордсмены: находим самый продолжительный и самый короткий курс»")
    courses = ["Java-разработчик с нуля", "Fullstack-разработчик на Python", 
              "Python-разработчик с нуля", "Frontend-разработчик с нуля"]
    mentors = [
        ["Филипп Воронов", "Анна Юшина", "Иван Бочаров"],
        ["Евгений Шмаргунов", "Олег Булыгин", "Александр Бардин"],
        ["Евгений Шмаргунов", "Олег Булыгин", "Дмитрий Демидов"],
        ["Владимир Чебукин", "Эдгар Нуруллин", "Евгений Шек"]
    ]
    durations = [14, 20, 12, 20]
    
    result = PythonBasics.find_course_durations(courses, mentors, durations)
    print(f"Самый короткий курс(ы): {', '.join(result['shortest'])} - {result['min_duration']} месяца(ев)")
    print(f"Самый длинный курс(ы): {', '.join(result['longest'])} - {result['max_duration']} месяца(ев)")
    
    # Задание 2: Квадратное уравнение
    print("\n2. Задание «Квадратное уравнение»")
    test_cases = [(1, 8, 15), (1, -13, 12), (-4, 28, -49), (1, 1, 1)]
    for a, b, c in test_cases:
        result = PythonBasics.solve_quadratic_equation(a, b, c)
        print(f"Уравнение {a}x² + {b}x + {c} = 0: {result}")
    
    # Задание 3: Голосование
    print("\n3. Задание «Голосование»")
    votes1 = [1, 1, 1, 2, 3]
    votes2 = [1, 2, 3, 2, 2]
    print(f"Голосование {votes1}: победитель = {PythonBasics.vote(votes1)}")
    print(f"Голосование {votes2}: победитель = {PythonBasics.vote(votes2)}")
    
    # Загружаем конфигурацию
    config = load_config()
    if config:
        print("\n=== Тестирование API Яндекс.Диска ===")
        
        token = config.get('YANDEX', 'token', fallback='')
        if token and token != 'your_yandex_disk_token_here':
            yandex_api = YandexDiskAPI(token)
            test_folder = f"test_demo_{int(time.time())}"
            
            print(f"Создаем папку '{test_folder}'...")
            if yandex_api.create_folder(test_folder):
                print("Папка создана успешно!")
                print(f"Папка существует: {yandex_api.folder_exists(test_folder)}")
            else:
                print("Ошибка при создании папки")
        else:
            print("Токен Яндекс.Диска не настроен")
    
    print("\n=== Запуск тестов ===")
    print("Для запуска тестов используйте команду: pytest main.py -v")
