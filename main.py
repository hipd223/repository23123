import os
import time
import ctypes
from PIL import Image
import service as svc
import customtkinter as ctk

ctypes.windll.shcore.SetProcessDpiAwareness(2)

# --------------- FONTS ---------------

current_dir = os.path.dirname(os.path.abspath(__file__))

font_regular = os.path.join(current_dir, 'fonts', 'Rubik-Regular.ttf')
font_bold = os.path.join(current_dir, 'fonts', 'Rubik-Bold.ttf')

# Загрузка шрифтов
ctypes.windll.gdi32.AddFontResourceW(font_regular)
ctypes.windll.gdi32.AddFontResourceW(font_bold)

# Обновление списка шрифтов
ctypes.windll.user32.PostMessageW(0xFFFF, 0x001D, 0, 0)

# ---------------- APP ----------------

app = ctk.CTk()
app.title("Конвертер валют")

WIDTH, HEIGHT = 900, 600

screen_w = app.winfo_screenwidth()
screen_h = app.winfo_screenheight()

x = (screen_w // 2) - (WIDTH // 2)
y = (screen_h // 2) - (HEIGHT // 2)

app.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
app.resizable(False, False)

BG = "#AAB5B3"

app.configure(fg_color=BG)

selected_currency = ctk.StringVar(value="RUB")
vcmd = (app.register(svc.validate_numbers), '%P')
rates = svc.get_rates()

# ---------------- TITLE ----------------

title_label = ctk.CTkLabel(
    app,
    text="Hello, please select a currency!",
    font=("Rubik", 38),
    text_color="black"
)
svc.start_animation(app, title_label)
title_label.pack(pady=(40, 70))

svc.switch_text(app, title_label)

# ------------------ ICON --------------------

icon_path = os.path.join(current_dir, 'img', 'icon.ico')
arrow_path = os.path.join(current_dir, 'img', 'arrow1.png')

app.iconbitmap(icon_path)

# ---------------- MAIN FRAME ----------------

main_frame = ctk.CTkFrame(
    app,
    fg_color="transparent"
)
main_frame.pack(fill="x", pady=40, padx=80)

main_frame.grid_columnconfigure((0, 1, 2), weight=1)

# ---------------- LEFT CARD ----------------

left_card = ctk.CTkFrame(
    main_frame,
    width=240,
    height=180,
    corner_radius=20,
    fg_color="transparent"
)

left_card.grid(row=0, column=0)

left_btn = ctk.CTkButton(
    left_card,
    text="RUB",
    width=220,
    height=90,
    corner_radius=18,
    border_width=3,
    fg_color="#E7C7CB",
    text_color="black",
    font=("Arial", 34, "bold")
)
left_btn.pack(pady=(0, 14))

left_entry = ctk.CTkEntry(
    left_card,
    width=220,
    height=45,
    corner_radius=12,
    fg_color="#8F7E7E",
    border_width=0,
    validate="key",
    validatecommand=vcmd,
    text_color="white",
    justify="center",
    font=("Rubik", 24)
)
left_entry.insert(0, "0")
left_entry.pack()

# ---------------- CENTER SWAP ----------------  

btn_image = ctk.CTkImage(
    light_image=Image.open(arrow_path),
    dark_image=Image.open(arrow_path),
    size=(48, 48)
)

swap_btn = ctk.CTkButton(
    main_frame,
    text="",
    image=btn_image,
    width=80,
    height=80,
    fg_color="transparent",
    hover_color="#98A3A1",
    text_color="black",
    font=("Arial", 56),
)

swap_btn.grid(row=0, column=1)

# ---------------- RIGHT CARD ----------------

right_card = ctk.CTkFrame(
    main_frame,
    width=240,
    height=180,
    corner_radius=20,
    fg_color="transparent"
)

right_card.grid(row=0, column=2)

right_btn = ctk.CTkButton(
    right_card,
    text="EUR",
    width=220,
    height=90,
    corner_radius=18,
    border_width=3,
    fg_color="#E7C7CB",
    text_color="black",
    font=("Arial", 34, "bold")
)
right_btn.pack(pady=(0, 14))

right_entry = ctk.CTkEntry(
    right_card,
    width=220,
    height=45,
    corner_radius=12,
    validate="key",
    validatecommand=vcmd,
    fg_color="#8F7E7E",
    border_width=0,
    text_color="white",
    justify="center",
    font=("Rubik", 24)
)
right_entry.insert(0, "0")
right_entry.pack()

# ----------- DROPDOWN FRAME -----------  

dropdown_frame = ctk.CTkFrame(
    app,
    width=220,
    corner_radius=15,
    fg_color="#E7C7CB"
)

popular = [
    "USD",
    "EUR",
    "RUB",
    "GBP",
    "JPY",
    "CNY",
    "KZT",
    "UAH",
    "TRY",
    "CHF"
]
currencies = [c for c in popular if c in rates]

dropdown_frame.lift()

app.bind(
    "<Button-1>",
    lambda e: svc.remove_focus(
        app=app,
        event=e,
        dropdown_frame=dropdown_frame
    )
)
# ---------------- INFO ----------------

info_label = ctk.CTkLabel(
    app,
    text=f"Курс обновлен в {time.strftime("%H:%M")}",
    font=("Rubik", 20),
    text_color="black",
    fg_color="transparent"
)

info_label.pack(pady=(115, 10))

# ---------------- FOOTER ----------------

footer = ctk.CTkLabel(
    app,
    text="Все данные предоставляются Exchange Rates API, разработчик не несет ответственности за возможные неточности курса",
    font=("Rubik", 13),
    text_color="#444444"
)

# Настройка функции кнопки через конфигур после объявления второй кнопки
swap_btn.configure(command=lambda: svc.switch_currs(left_btn, right_btn, left_entry, right_entry))

# Привязка на вычисление по деактивации клавиши клавиатуры
left_entry.bind(
    "<KeyRelease>", 
    lambda event: svc.convert(
        source_entry=left_entry, 
        target_entry=right_entry, 
        source_btn=left_btn, 
        target_btn=right_btn, 
        rates_dict=rates
    )
)

left_btn.configure(
    command=lambda: svc.open_dropdown(
        app,
        left_btn,
        dropdown_frame,
        currencies,
        ctk
    )
)

right_btn.configure(
    command=lambda: svc.open_dropdown(
        app,
        right_btn,
        dropdown_frame,
        currencies,
        ctk
    )
)

footer.pack(side="bottom", pady=10)

app.mainloop()