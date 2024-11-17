import tkinter as tk
import os
import subprocess
import sys
import git
from tkinter import ttk



# Оновлення коду при запуску програми.
# URL вашого репозиторію на GitHub
GITHUB_REPO = "https://github.com/goldplayer/u_24_exe_.git"
# Локальний шлях до директорії з репозиторієм
LOCAL_REPO_PATH = os.path.join(os.getcwd(), "repo")

def update_from_github(repo_url, local_path):
    """
    Завантажує або оновлює репозиторій GitHub на локальній машині.
    """
    if not os.path.exists(local_path):
        print("Клонуємо репозиторій...")
        git.Repo.clone_from(repo_url, local_path)
    else:
        print("Оновлюємо репозиторій...")
        repo = git.Repo(local_path)
        origin = repo.remotes.origin
        origin.pull()
    print("Репозиторій синхронізовано.")
    print("Содержимое директории 'repo':", os.listdir(local_path))

def restart_program():
    """
    Перезапускає оновлену версію програми.
    """
    script_path = os.path.join(LOCAL_REPO_PATH, "test_1.py")
    print(f"Пытаемся запустить файл: {script_path}")
    if os.path.exists(script_path):
        subprocess.Popen([sys.executable, script_path])
        sys.exit(0)
    else:
        print(f"Файл {script_path} не знайдено у репозиторії.")
        sys.exit(1)

if __name__ == "__main__":
    try:
        update_from_github(GITHUB_REPO, LOCAL_REPO_PATH)
        restart_program()
    except Exception as e:
        print(f"Помилка: {e}")



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

    
}

house_types = ["Квартира", "Приватний будинок", "Таунхаус", "Дача", "Пусто"]
garage_options = ["Немає гаражних місць", "2", "5", "10", "14", "20", "Пусто"]
districts = ["Центр", "Північ", "Південь", "Схід", "Захід", "Пусто"]

def generate_announcement():
    global announcement
    if not action.get():
        show_popup("Будь ласка, оберіть дію!")
        return
    if not category_var.get():
        show_popup("Будь ласка, оберіть категорію!")
        return

    type_text = "Куплю" if action.get() == "Куплю" else "Продам"
    category = category_var.get()

    if category == "Авто":
        brand_text = brand.get() or "Пусто"
        model_text = model.get() or "Пусто"
        ft_text = "З повним комплектом деталей." if ft_var.get() else ""
        price_text = f"Ціна: {price.get()} грн." if price.get() else ""
        announcement = f"{type_text} т/з марки {brand_text} {model_text}. {ft_text} {price_text}"

    elif category == "Дім":
        house_type = house_type_var.get() or "Пусто"
        garage = garage_var.get() or "Пусто"
        district = district_var.get() or "Пусто"
        announcement = (
            f"{type_text} будинок типу '{house_type}', "
            f"гаражні місця: {garage}, район: {district}."
        )

    print("Функція generate_announcement викликається")
    print(f"Вибрана дія: {action.get()}, категорія: {category_var.get()}")

    # Виводимо у консоль для перевірки
    print(f"Generated Announcement: {announcement}")

    # Копіюємо текст у буфер обміну
    root.clipboard_clear()
    root.clipboard_append(announcement)
    root.update()  # Оновлення буфера обміну

    # Виводимо оголошення на екран
    result_label.config(text=announcement)

    # Показуємо вспливаюче повідомлення
    show_popup("Оголошення скопійоване в буфер обміну!")

# Функція для вспливаючого повідомлення
def show_popup(message):
    popup = tk.Toplevel(root)
    popup.geometry("300x50")
    popup.overrideredirect(True)
    popup.attributes("-topmost", True)
    tk.Label(popup, text=message, font=("Arial", 10), bg="lightyellow", fg="black").pack(fill="both", expand=True)

    x = root.winfo_x() + root.winfo_width() // 2 - 150
    y = root.winfo_y() + root.winfo_height() // 2 - 25
    popup.geometry(f"+{x}+{y}")
    popup.after(2000, popup.destroy)

# Функція для оновлення списку моделей авто
def update_models(*args):
    selected_brand = brand.get()
    if selected_brand in auto_data:
        model_menu["values"] = auto_data[selected_brand]
        model.set("")
    else:
        model_menu["values"] = []

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
        brand.trace("w", update_models)
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

    elif selected_category == "Дім":
        # Вибір типу будинку
        tk.Label(main_frame, text="Оберіть тип будинку:", font=("Arial", 12)).pack(pady=5)
        global house_type_var
        house_type_var = tk.StringVar(value="")
        house_type_menu = ttk.Combobox(main_frame, textvariable=house_type_var, values=house_types, font=("Arial", 12))
        house_type_menu.pack(pady=5)

        # Вибір кількості гаражних місць
        tk.Label(main_frame, text="Кількість гаражних місць:", font=("Arial", 12)).pack(pady=5)
        global garage_var
        garage_var = tk.StringVar(value="")
        garage_menu = ttk.Combobox(main_frame, textvariable=garage_var, values=garage_options, font=("Arial", 12))
        garage_menu.pack(pady=5)

        # Вибір району
        tk.Label(main_frame, text="Оберіть район:", font=("Arial", 12)).pack(pady=5)
        global district_var
        district_var = tk.StringVar(value="")
        district_menu = ttk.Combobox(main_frame, textvariable=district_var, values=districts, font=("Arial", 12))
        district_menu.pack(pady=5)

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

# Функція для показу категорій
def show_categories():
    for widget in main_frame.winfo_children():
        widget.destroy()
    tk.Label(main_frame, text="Оберіть категорію:", font=("Arial", 14)).pack(pady=10)
    for cat in ["Авто", "Дім"]:
        tk.Button(main_frame, text=cat, font=("Arial", 12), command=lambda c=cat: show_details(c)).pack(pady=5)

# Основне вікно
root = tk.Tk()
root.title("Редактор оголошень")
root.geometry("400x500")

# Змінні
action = tk.StringVar(value="")
category_var = tk.StringVar(value="")
announcement = ""

# Головна рамка
main_frame = tk.Frame(root)
main_frame.pack(expand=True, fill="both")

# Початковий екран
main_screen()

root.mainloop()