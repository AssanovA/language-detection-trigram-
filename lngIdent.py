import csv
from collections import defaultdict
import re


def preprocess_text(text):
    # Удаляем ненужные символы и приводим к нижнему регистру
    text = re.sub(r'[^a-zA-Zа-яА-ЯёЁ ]', '', text.lower())
    return text


def generate_trigrams(text):
    # Генерируем триграммы из текста
    trigrams = []
    words = text.split()
    for word in words:
        if len(word) < 3:
            continue
        for i in range(len(word) - 2):
            trigrams.append(word[i:i + 3])
    return trigrams


def train_language_model(csv_file):
    # Обучение модели на основе данных из CSV-файла
    language_model = defaultdict(lambda: defaultdict(int))
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Пропускаем заголовок (если есть)
        for row in csv_reader:
            text = row[0]  # Получаем текст из первого столбца
            language = row[1]  # Получаем язык из второго столбца
            preprocessed_text = preprocess_text(text)
            trigrams = generate_trigrams(preprocessed_text)
            for trigram in trigrams:
                language_model[language][trigram] += 1
    return language_model


def identify_language(input_text, language_model):
    preprocessed_text = preprocess_text(input_text)
    trigrams = generate_trigrams(preprocessed_text)
    scores = defaultdict(int)
    for trigram in trigrams:
        for language, trigram_counts in language_model.items():
            scores[language] += trigram_counts[trigram]

    identified_language = max(scores, key=scores.get)
    return identified_language


# Пример использования программы
csv_file = 'C:/Users/user/Desktop/LangDet.csv'
#https://www.kaggle.com/datasets/basilb2s/language-detection
input_text = ''

model = train_language_model(csv_file)
identified_language = identify_language(input_text, model)

print(f"The identified language is: {identified_language}")
