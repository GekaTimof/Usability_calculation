import tkinter as tk
from tkinter import ttk

note_len = 5

# Список параметров и их весов
parameters = [
    {"name": "  Время выполнения", "scale": (1, 10), "weight": 2},
    {"name": "  Кол-во кликов", "scale": (1, 10), "weight": 2},
    {"name": "  Количество попыток достичь цели", "scale": (1, 5), "weight": 3},
    {"name": "  Количество сценариев для достижения цели", "scale": (1, 5), "weight": 1},
    {"name": "  Простота выполнения", "scale": (1, 10), "weight": 3},
    {"name": "  Удовлетворённость респондента", "scale": (1, 10), "weight": 2},
    {"name": "  Степень важности выявленных проблем", "scale": (1, 5), "weight": 3}
]

# Функция для расчета итоговой метрики
def calculate_metric():
    total_score = 0
    total_weight = 0

    # Обход каждого параметра и соответствующего слайдера
    for param_name, (slider, value_label) in sliders.items():
        value = int(slider.get())  # Получение значения слайдера как целого числа
        value_label.config(text=str(value))  # Обновление метки с текущим значением

        weight = next(param["weight"] for param in parameters if param["name"] == param_name)
        max_value = next(param["scale"][1] for param in parameters if param["name"] == param_name)
        total_score += value * weight
        total_weight += max_value * weight

    # Рассчет итоговой метрики
    sum_metric = total_score / total_weight if total_weight > 0 else 0
    result_label.config(text=f"Суммарная метрика (SUM): {sum_metric*100:.1f}% ")

# Создание главного окна
root = tk.Tk()
root.title("Рассчет итоговой метрики")

# Словарь для хранения слайдеров и меток значений
sliders = {}

# Заметка о том как оцениваются метрики
label = ttk.Label(root, text=f"Оценивание метрик: \n    Min значение - полностью НЕ удовлетворен, \n    Max значение - полностью удовлетворен \n\nВыберите нужные значения метрик:")
label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

# Создание слайдеров для каждого параметра
for index, param in enumerate(parameters):
    label = ttk.Label(root, text=f"{param['name']} (Вес: {param['weight']})")
    label.grid(row=index + note_len, column=0, padx=10, pady=5, sticky="w")

    # Создание слайдера (ползунка)
    slider = ttk.Scale(root, from_=param["scale"][0], to=param["scale"][1], orient="horizontal",
                        command=lambda val, param_name=param['name']: update_value_label(val, param_name))
    slider.grid(row=index + note_len, column=1, padx=10, pady=5)

    # Установка начального значения в середину диапазона
    slider.set((param["scale"][0] + param["scale"][1]) / 2)

    # Создание метки для отображения текущего значения
    value_label = ttk.Label(root, text=str(int(slider.get())))  # Изначально показываем целое число
    value_label.grid(row=index + note_len, column=2, padx=10, pady=5)

    # Сохранение слайдера и метки для последующего доступа, используя имя параметра
    sliders[param['name']] = (slider, value_label)

# Функция для обновления метки с текущим значением
def update_value_label(value, param_name):
    sliders[param_name][1].config(text=str(int(float(value))))  # Обновляем метку с целым числом

# Кнопка для расчета метрики
calculate_button = ttk.Button(root, text="Рассчитать метрику", command=calculate_metric)
calculate_button.grid(row=len(parameters) + note_len, column=0, columnspan=3, pady=20)

# Метка для отображения результата
result_label = ttk.Label(root, text="Суммарная метрика (SUM): -")
result_label.grid(row=len(parameters) + note_len + 1, column=0, columnspan=3, pady=10)

# заметка о том что означает метрика
label = ttk.Label(root, text=f"* Чем значение SUM ближе к 100% тем лучше")
label.grid(row=len(parameters) + note_len + 2, column=0, columnspan=3, pady=10)

# Запуск главного цикла окна
root.mainloop()
