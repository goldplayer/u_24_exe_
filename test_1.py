import tkinter as tk
import os
import subprocess
import sys
import git
from tkinter import ttk

def update_from_github(repo_url, local_path):
    if os.path.exists(local_path):
        repo = git.Repo(local_path)
        repo.remotes.origin.pull()
        print("Код оновлено з GitHub.")
    else:
        git.Repo.clone_from(repo_url, local_path)
        print("Код завантажено з GitHub.")

def restart_application(script_path):
    print("Перезапускаємо програму...")
    subprocess.Popen([sys.executable, script_path])
    sys.exit()

if __name__ == "__main__":
    # URL вашого GitHub репозиторію
    GITHUB_REPO = "https://github.com/username/repo-name.git"
    LOCAL_REPO_PATH = "./repo"

    # Завантажуємо або оновлюємо репозиторій
    update_from_github(GITHUB_REPO, LOCAL_REPO_PATH)

    # Запускаємо основний скрипт із репозиторію
    MAIN_SCRIPT = os.path.join(LOCAL_REPO_PATH, "main.py")
    restart_application(MAIN_SCRIPT)

# Дані для автомобілів
auto_data = {
    "Obey(Audi)": ["A6", "TTS", "RS6 Avant", "RS3", "RS6 Avant", "RS7 2013", "S4 B6", "RS6 C8 Avant", "Q7", "R8",],
    "UMA(BMW)": [
        "760i E65",
        "X5 M", 
        "M2 Coupe 2018",
        "5 Series E60", 
        "5 Series 535", 
        "E34", 
        "M5", 
        "I8", 
        "X6 E71", 
        "X6 F96", 
        "M5 F90 Competition", 
        "M4", 
        "M4G80"
        ],
       "Benefactor (Mercedes)": [
        "Dubsta X66",
        "G63 AMG",
        "XLS",
        "Schwartzer",
        "Schafter V12",
        "Surano",
        "Superd",
        "Dubsta",
        "Schlagen GT"
    ],
    "Enus(Bentley)": ["Continental GT", "Betayga"],
    "Urus(Lamborghini)":["Urus", "Veneno","Aventador", "Terzo Milennio", "SIAN FKP 37"],
    "Annis (Nissan)": ["S30", "Qashqai 2016", "GT-R", "Skyline R34"],
    "Pfister (Porshe)": ["911 RS", "811", "Comet", "Neon", "Taycan", "944", "Panamera Turbo", ""],
    "Dewbauchee (AstonMartin)": ["DB11"],
    "Bravado ()":["Landstalker", "Gresley", "Gauntlet", "Buffalo S", ""]

    # Додайте інші марки і моделі
}

# Функція для створення оголошення
def generate_announcement():
    global announcement
    type_text = "Куплю" if action.get() == "Куплю" else "Продам"
    brand_text = brand.get()
    model_text = model.get()
    ft_text = "З повним комплектом деталей." if ft_var.get() else ""
    price_text = f"Ціна: {price.get()} грн." if price.get() else ""
    announcement = f"{type_text} т/з марки {brand_text} {model_text}. {ft_text} {price_text}"
    
    # Копіюємо текст у буфер обміну
    root.clipboard_clear()
    root.clipboard_append(announcement)
    root.update()  # Оновлення буфера обміну

    # Показуємо вспливаюче повідомлення
    show_popup("Оголошення скопійоване в буфер обміну!")
    
    # Оновлення тексту результату
    result_label.config(text=announcement)

# Функція для вспливаючого повідомлення
def show_popup(message):
    popup = tk.Toplevel(root)
    popup.geometry("300x50")
    popup.overrideredirect(True)  # Забирає рамку вікна
    popup.attributes("-topmost", True)  # Завжди поверх інших вікон
    tk.Label(popup, text=message, font=("Arial", 10), bg="lightyellow", fg="black").pack(fill="both", expand=True)
    
    # Розташування по центру головного вікна
    x = root.winfo_x() + root.winfo_width() // 2 - 150
    y = root.winfo_y() + root.winfo_height() // 2 - 25
    popup.geometry(f"+{x}+{y}")
    
    # Автоматичне закриття через 2 секунди
    popup.after(2000, popup.destroy)

# Функція для оновлення списку моделей
def update_models(*args):
    selected_brand = brand.get()
    if selected_brand in auto_data:
        model_menu["values"] = auto_data[selected_brand]
        model.set("")  # Скидаємо вибір моделі
    else:
        model_menu["values"] = []

# Функція для показу категорій
def show_categories():
    for widget in main_frame.winfo_children():
        widget.destroy()
    tk.Label(main_frame, text="Оберіть категорію:", font=("Arial", 14)).pack(pady=10)
    for cat in ["Авто", "Бізнес", "Речі"]:
        tk.Button(main_frame, text=cat, font=("Arial", 12), command=lambda c=cat: show_details(c)).pack(pady=5)

# Функція для показу деталей
def show_details(selected_category):
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    tk.Label(main_frame, text=f"Категорія: {selected_category}", font=("Arial", 14)).pack(pady=10)

    if selected_category == "Авто":
        # Вибір марки
        tk.Label(main_frame, text="Оберіть марку:", font=("Arial", 12)).pack(pady=5)
        global brand
        brand = tk.StringVar(value="")
        brand.trace("w", update_models)  # Слідкуємо за зміною вибору марки
        global brand_menu
        brand_menu = ttk.Combobox(main_frame, textvariable=brand, values=list(auto_data.keys()), font=("Arial", 12))
        brand_menu.pack(pady=5)

        # Вибір моделі
        tk.Label(main_frame, text="Оберіть модель:", font=("Arial", 12)).pack(pady=5)
        global model
        model = tk.StringVar(value="")
        global model_menu
        model_menu = ttk.Combobox(main_frame, textvariable=model, font=("Arial", 12))
        model_menu.pack(pady=5)
    
    # Комплектація
    global ft_var
    ft_var = tk.BooleanVar(value=False)
    tk.Checkbutton(main_frame, text="З повним комплектом деталей", variable=ft_var, font=("Arial", 12)).pack(pady=5)

    # Введення ціни
    tk.Label(main_frame, text="Ціна (грн):", font=("Arial", 12)).pack(pady=5)
    global price
    price = tk.Entry(main_frame, font=("Arial", 12))
    price.pack(pady=5)

    # Кнопка для генерації оголошення
    tk.Button(main_frame, text="Згенерувати оголошення", font=("Arial", 12), command=generate_announcement).pack(pady=10)

    # Поле для результату
    global result_label
    result_label = tk.Label(main_frame, text="", font=("Arial", 12), fg="green", wraplength=300)
    result_label.pack(pady=5)

# Головний екран
def main_screen():
    for widget in main_frame.winfo_children():
        widget.destroy()

    tk.Label(main_frame, text="Оберіть дію:", font=("Arial", 14)).pack(pady=10)
    for action_text in ["Куплю", "Продам"]:
        tk.Button(main_frame, text=action_text, font=("Arial", 12), command=lambda a=action_text: set_action(a)).pack(pady=5)

# Функція для збереження вибраної дії
def set_action(selected_action):
    global action
    action.set(selected_action)
    show_categories()

# Основне вікно
root = tk.Tk()
root.title("Редактор оголошень")
root.geometry("400x400")

# Змінні
action = tk.StringVar(value="")
announcement = ""

# Головна рамка
main_frame = tk.Frame(root)
main_frame.pack(expand=True, fill="both")

# Початковий екран
main_screen()

root.mainloop()