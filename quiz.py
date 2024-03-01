import pygame
import sys
import random

pygame.init()

SCREEN = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Quiz App")

BG_COLOUR = "#0a092d"
FLASHCARD_COLOUR = "#2e3856"
FLIPPED_COLOUR = "#595e6d"
SELECTED_COLOUR = "#ff0000"  # Цвет для выбранной сложности

FONT = pygame.font.SysFont("Arial", 30)

pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

# Меню
menu_title = FONT.render("Press Enter to Start", True, "white")
menu_title_rect = menu_title.get_rect(center=(400, 400))

difficulty_buttons = [
    {"text": "Easy", "rect": pygame.Rect(150, 500, 100, 50)},
    {"text": "Medium", "rect": pygame.Rect(350, 500, 100, 50)},
    {"text": "Hard", "rect": pygame.Rect(550, 500, 100, 50)}
]

selected_difficulty = None

SCREEN.fill(BG_COLOUR)
SCREEN.blit(menu_title, menu_title_rect)
pygame.display.update()

# Ожидание начала игры и выбора сложности
waiting_for_start = True
while waiting_for_start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if selected_difficulty is not None:
                waiting_for_start = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for btn in difficulty_buttons:
                if btn["rect"].collidepoint(event.pos):
                    selected_difficulty = btn["text"]

    # Отображение кнопок сложности в меню
    for btn in difficulty_buttons:
        btn_color = SELECTED_COLOUR if selected_difficulty == btn["text"] else (255, 255, 255)
        pygame.draw.rect(SCREEN, btn_color, btn["rect"], border_radius=10)
        btn_text = FONT.render(btn["text"], True, (0, 0, 0))
        btn_text_rect = btn_text.get_rect(center=btn["rect"].center)
        SCREEN.blit(btn_text, btn_text_rect)

    pygame.display.update()

# Генерация вопросов и ответов в зависимости от выбранной сложности
if selected_difficulty == "Easy":
    quiz_data = {
        "Translate 'Cat'": "Кошка",
        "Translate 'Dog'": "Собака",
        "Translate 'Sun'": "Солнце",
        "Translate 'Book'": "Книга",
        "Translate 'Water'": "Вода",
        "Translate 'House'": "Дом",
        "Translate 'Friend'": "Друг",
        "Translate 'Food'": "Еда",
        "Translate 'Family'": "Семья",
        "Translate 'School'": "Школа",
        "Translate 'Car'": "Автомобиль",
        "Translate 'Music'": "Музыка",
        "Translate 'City'": "Город",
        "Translate 'Tree'": "Дерево",
        "Translate 'Time'": "Время"
    }
elif selected_difficulty == "Medium":
    quiz_data = {
        "Translate 'Computer'": "Компьютер",
        "Translate 'Language'": "Язык",
        "Translate 'Travel'": "Путешествие",
        "Translate 'Health'": "Здоровье",
        "Translate 'Work'": "Работа",
        "Translate 'Nature'": "Природа",
        "Translate 'Money'": "Деньги",
        "Translate 'Sport'": "Спорт",
        "Translate 'Art'": "Искусство",
        "Translate 'History'": "История",
        "Translate 'Science'": "Наука",
        "Translate 'Film'": "Фильм",
        "Translate 'City'": "Город",
        "Translate 'Friend'": "Друг",
        "Translate 'Family'": "Семья"
    }
else:  # Hard
    quiz_data = {
        "Translate 'Blockchain'": "Цепочка блоков",
        "Translate 'Algorithm'": "Алгоритм",
        "Translate 'Encryption'": "Шифрование",
        "Translate 'Artificial Intelligence'": "Искусственный интеллект",
        "Translate 'Cybersecurity'": "Кибербезопасность",
        "Translate 'Quantum Computing'": "Квантовые вычисления",
        "Translate 'Virtual Reality'": "Виртуальная реальность",
        "Translate 'Biotechnology'": "Биотехнологии",
        "Translate 'Space Exploration'": "Исследование космоса",
        "Translate 'Nanotechnology'": "Нанотехнологии",
        "Translate 'Renewable Energy'": "Возобновляемая энергия",
        "Translate 'Genetic Engineering'": "Генная инженерия",
        "Translate 'Neuroscience'": "Нейронаука",
        "Translate 'Quantum Physics'": "Квантовая физика",
        "Translate 'Astrophysics'": "Астрофизика"
    }

# Выбор случайных вопросов и ответов
selected_items = random.sample(list(quiz_data.items()), 5)
selected_quiz_data = dict(selected_items)

current_question = ""
current_answer = ""
card_turned = False
index = 0

# Время (в миллисекундах) для автоматического переворота карточки в сложном режиме
AUTO_FLIP_TIME = 4000  # 2 секунды для переворота
# Время (в миллисекундах) через которое произойдет смена вопроса
QUESTION_CHANGE_TIME = 5500  # 3 секунды

# Запоминание времени начала таймеров
start_flip_time = pygame.time.get_ticks()
start_question_change_time = pygame.time.get_ticks()
start_hard_mode_timer = pygame.time.get_ticks()

stop_time = False

time_remaining = 0

def animate_question_change():
    fade_surface = pygame.Surface((500, 300))  # Размер области карточки
    fade_surface.fill((73, 81, 107))

    for alpha in range(0, 255, 10):
        fade_surface.set_alpha(alpha)
        card_rect = pygame.Rect(150, 250, 500, 300)
        SCREEN.blit(fade_surface, card_rect)
        pygame.display.update(card_rect)
        pygame.time.delay(20)

while True:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                card_turned = not card_turned
                stop_time = not stop_time
            elif pygame.key.get_pressed()[pygame.K_RIGHT] and index < len(selected_quiz_data) - 1:
                index += 1
                card_turned = False
                start_question_change_time = pygame.time.get_ticks()
                start_flip_time = pygame.time.get_ticks()
                stop_time = False
                animate_question_change()
            elif pygame.key.get_pressed()[pygame.K_LEFT] and index > 0:
                index -= 1
                card_turned = False
                start_question_change_time = pygame.time.get_ticks()
                start_flip_time = pygame.time.get_ticks()
                stop_time = False
                animate_question_change()
    time_remaining = 4 - ((current_time - start_flip_time)) // 1000
    # Проверка времени для автоматического переворота карточки в сложном режиме
    if selected_difficulty == "Hard" and not card_turned and current_time - start_flip_time >= AUTO_FLIP_TIME and stop_time == False:
        card_turned = True
        start_flip_time = pygame.time.get_ticks()

    # Проверка времени для смены вопроса
    if selected_difficulty == "Hard" and current_time - start_question_change_time >= QUESTION_CHANGE_TIME and stop_time == False:
        animate_question_change()
        if index < len(selected_quiz_data) - 1:
            index += 1
        card_turned = False
        start_question_change_time = pygame.time.get_ticks()
        start_flip_time = pygame.time.get_ticks()


    # Отображение текущего вопроса или ответа
    current_question = list(selected_quiz_data)[index]
    current_answer = list(selected_quiz_data.values())[index]
    current_question_object = FONT.render(current_question, True, "white")
    current_question_rect = current_question_object.get_rect(center=(400, 400))
    current_answer_object = FONT.render(current_answer, True, "white")
    current_answer_rect = current_answer_object.get_rect(center=(400, 400))
    current_index_object = FONT.render(f"{index + 1}/{len(selected_quiz_data)}", True, "white")
    current_index_rect = current_index_object.get_rect(center=(400, 600))
    timer_object = FONT.render(f"Next Flip in: {time_remaining} seconds", True, "white")
    timer_rect = timer_object.get_rect(center=(400, 750))

    # Отображение текущего индекса
    SCREEN.fill(BG_COLOUR)
    if not card_turned:
        pygame.draw.rect(SCREEN, FLASHCARD_COLOUR, (150, 250, 500, 300), border_radius=10)
        SCREEN.blit(current_question_object, current_question_rect)
        if selected_difficulty == "Hard":
            SCREEN.blit(timer_object, timer_rect)

    else:
        pygame.draw.rect(SCREEN, FLIPPED_COLOUR, (150, 250, 500, 300), border_radius=10)
        SCREEN.blit(current_answer_object, current_answer_rect)

    # Отображение текущего индекса
    SCREEN.blit(current_index_object, current_index_rect)

    pygame.display.update()
