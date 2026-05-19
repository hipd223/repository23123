import requests

# Запрос курса
def get_rates():
    url = f"https://v6.exchangerate-api.com/v6/84d992cfc0c6ae77f4e22aa7/latest/USD"

    try:
        response = requests.get(url)
        data = response.json()
        if data.get('result') == "success":
            return data["conversion_rates"]
    except Exception as e:
        print('Ошибка:', e)
        return None
    

# Функция конвертации
def convert(source_entry, target_entry, source_btn, target_btn, rates_dict):

    raw_text = source_entry.get()
    if not raw_text:
        target_entry.delete(0, "end")
        return

    curr_from = source_btn.cget("text")
    curr_to = target_btn.cget("text")

    if not rates_dict or curr_from not in rates_dict or curr_to not in rates_dict:
        return
    
    try:
        clean_text = raw_text.replace(",", ".")
        amount = float(clean_text)

        rate_from = rates_dict[curr_from]
        rate_to = rates_dict[curr_to]

        result = amount * (rate_to / rate_from)

        target_entry.delete(0, "end")
        target_entry.insert(0, str(round(result, 2)))

    except ValueError:
        pass

# Логика фраз
phrases = [
    "Привет, выберите валюту",
    "Hello, please select a currency!",
    "Добро пожаловать в конвертер",
    "Выберите пару валют"
]

print(len(phrases))

current_text = 0
animation_timer = 0

# Цвет фона
BG_COLOR = "#AAB5B3"

# Цвет текста
TEXT_COLOR = "#000000"

def hex_to_rgb(hex_color):
    hex_color = hex_color.strip("#")  # Вырезаем "#"
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))  # возвращаем кортеж с тремя числами, которые являются тем же цветом в RBG из HEX

def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb # шаблон для преобразования хекса в ргб

def interpolate(c1, c2, t):
    return tuple(
        int(c1[i] + (c2[i] - c1[i]) * t)
        for i in range(3)
    )

def fade_out(app, label, step=0):
    global animation_timer
    bg = hex_to_rgb(BG_COLOR)
    fg = hex_to_rgb(TEXT_COLOR)
    t = step / 10

    color = interpolate(fg, bg, t)
    label.configure(text_color=rgb_to_hex(color))

    if step < 10:
        animation_timer = app.after(40, lambda: fade_out(app, label, step + 1))
    else:
        switch_text(app, label)

def fade_in(app, label, step=0):
    global animation_timer
    bg = hex_to_rgb(BG_COLOR)
    fg = hex_to_rgb(TEXT_COLOR)
    t = step / 10

    color = interpolate(bg, fg, t)
    label.configure(text_color=rgb_to_hex(color))

    if step < 10:
        animation_timer = app.after(40, lambda: fade_in(app, label, step + 1))
    else:
        animation_timer = app.after(2500, lambda: fade_out(app, label))

def switch_text(app, label):
    global current_text, animation_timer

    # Отменяем старый таймер, если он остался в памяти
    if animation_timer is not None:
        app.after_cancel(animation_timer)
        animation_timer = None

    current_text += 1

    if current_text >= len(phrases):
        current_text = 0

    label.configure(text=phrases[current_text])
    fade_in(app, label)

def start_animation(app, label):
    label.configure(text=phrases[0])
    fade_in(app, label)


is_open = False

def select_currency(button, dropdown_frame, currency):
    button.configure(text=currency)
    close_dropdown(dropdown_frame)

def open_dropdown(app, button, dropdown_frame, currencies, ctk):

    global is_open

    if is_open:
        close_dropdown(dropdown_frame)

    # очищаем старые элементы
    for widget in dropdown_frame.winfo_children():
        widget.destroy()

    # scrollable frame
    scroll_frame = ctk.CTkScrollableFrame(
        dropdown_frame,
        width=180,
        height=250,
        fg_color="#E7C7CB"
    )

    scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

    for curr in currencies:

        btn = ctk.CTkButton(
            scroll_frame,
            text=curr,
            height=40,
            corner_radius=12,
            fg_color="transparent",
            hover_color="#DDB8BE",
            text_color="black",
            font=("Rubik", 18)
        )

        btn.configure(
            command=lambda c=curr: select_currency(button, dropdown_frame, c)
        )

        btn.pack(fill="x", padx=4, pady=2)

    # позиция dropdown под кнопкой
    x = button.winfo_rootx() - app.winfo_rootx()
    y = button.winfo_rooty() - app.winfo_rooty() + button.winfo_height() + 5

    dropdown_frame.place(x=x, y=y)

    is_open = True

def close_dropdown(dropdown_frame):
    global is_open
    dropdown_frame.place_forget()
    is_open = False

def remove_focus(app, event, dropdown_frame=None):

    clicked_widget = event.widget


    if 'entry' not in str(clicked_widget).lower():
        app.focus_set()


    if "button" in str(clicked_widget).lower():
        return

    if dropdown_frame and is_open:

        x1 = dropdown_frame.winfo_rootx()
        y1 = dropdown_frame.winfo_rooty()

        x2 = x1 + dropdown_frame.winfo_width()
        y2 = y1 + dropdown_frame.winfo_height()

        mouse_x = event.x_root
        mouse_y = event.y_root

        if not (x1 <= mouse_x <= x2 and y1 <= mouse_y <= y2):
            close_dropdown(dropdown_frame)

def switch_currs(btn1, btn2, entry1, entry2):
    btn1_text = btn1.cget("text")
    btn2_text = btn2.cget("text")
    
    btn1.configure(text=btn2_text)
    btn2.configure(text=btn1_text)

    entry1_text = entry1.get()
    entry2_text = entry2.get()

    entry1.delete(0, "end")
    entry1.insert(0, entry2_text)

    entry2.delete(0, "end")
    entry2.insert(0, entry1_text)

def validate_numbers(text):
    if text == "":
        return True
    
    normalized_text = text.replace(",", ".")

    if normalized_text.count(".") > 1:
        return False
    
    clean_text = normalized_text.replace(".", "")
    return clean_text.isdigit()