import flet as ft
from datetime import datetime
from database import init_db, add_name, get_history, delete_last, delete_all

def main(page: ft.Page):
    page.title = "Приветствия с историей"
    page.theme_mode = ft.ThemeMode.LIGHT

    # Инициализация базы данных
    init_db()

    name_input = ft.TextField(label="Введите ваше имя", width=300)
    greeting_text = ft.Column()  # Для отображения истории

    def update_history():
        """Обновление колонки с историей приветствий"""
        greeting_text.controls.clear()
        history = get_history()
        for idx, (id, name, created_at) in enumerate(history):
            if idx == len(history) - 1:  # последнее имя подсвечено
                text_control = ft.Text(
                    spans=[
                        ft.TextSpan(text=f"{created_at} Привет ",
                                    style=ft.TextStyle(color=ft.Colors.BLACK)),
                        ft.TextSpan(text=name,
                                    style=ft.TextStyle(color=ft.Colors.BLUE, weight="bold"))
                    ]
                )
            else:
                text_control = ft.Text(f"{created_at} Привет {name}")
            greeting_text.controls.append(text_control)
        page.update()

    def greet(e):
        name = name_input.value.strip() or "Гость"
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        add_name(name, created_at)
        name_input.value = ""
        update_history()

    def delete_last_greeting(e):
        history = get_history()
        if not history:
            page.dialog = ft.AlertDialog(title=ft.Text("История пуста!"))
            page.dialog.open = True
            page.update()
            return
        delete_last()
        update_history()

    def sort_history(e):
        history = get_history()
        sorted_history = sorted(history, key=lambda x: x[1].lower())
        delete_all()
        for id, name, created_at in sorted_history:
            add_name(name, created_at)
        update_history()

    # Кнопки
    greet_button = ft.ElevatedButton("Поздороваться", on_click=greet)
    delete_button = ft.ElevatedButton("Удалить последнее", on_click=delete_last_greeting,
                                      bgcolor=ft.Colors.RED)
    sort_button = ft.ElevatedButton("Сортировать по алфавиту", on_click=sort_history)

    page.add(
        name_input,
        ft.Row([greet_button, delete_button, sort_button],
               alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        ft.Divider(),
        greeting_text
    )

    update_history()

ft.app(target=main)