import flet as ft
import datetime
from numerology_logic import NumerologyCalculator as calc

def main(page: ft.Page):
    page.title = "AI Nomerology"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 800
    page.bgcolor = "#0F0F1F"  # Space Dark
    
    # Custom Styles
    PRIMARY_COLOR = "#7B61FF" # Cosmic Purple
    SECONDARY_COLOR = "#FFD700" # Golden
    
    def calculate_click(e):
        if not dob_input.value:
            dob_input.error_text = "Введите дату"
            page.update()
            return
            
        try:
            # Simple validation check
            datetime.datetime.strptime(dob_input.value, "%d.%m.%Y")
            dob = dob_input.value
            
            # Life Path
            lp_data = calc.calculate_life_path(dob)
            lp_val = lp_data['value']
            interpretation = calc.get_interpretation(lp_val)
            
            # Update UI with results
            results_column.controls.clear()
            results_column.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"Число Жизненного Пути: {lp_val}", size=24, color=SECONDARY_COLOR, weight="bold"),
                        ft.Divider(color=PRIMARY_COLOR),
                        ft.Text(interpretation, size=16, color="white"),
                    ]),
                    padding=20,
                    border_radius=15,
                    bgcolor="#1A1A2E",
                    margin=ft.margin.only(top=20)
                )
            )
            
            # Show Ad Placeholder (For Play Market monetization strategy)
            results_column.controls.append(
                ft.Container(
                    content=ft.Text("ADVERTISEMENT SPACE", color="#444444", size=12),
                    alignment=ft.alignment.center,
                    height=50,
                    bgcolor="#050505",
                    margin=ft.margin.only(top=10)
                )
            )
            
            page.update()
            
        except ValueError:
            dob_input.error_text = "Формат: ДД.ММ.ГГГГ"
            page.update()

    # UI Components
    header = ft.Container(
        content=ft.Column([
            ft.Text("AI NOMEROLOGY", size=32, weight="bold", color=PRIMARY_COLOR, italic=True),
            ft.Text("Твой цифровой код судьбы", size=14, color="#AAAAAA"),
        ], horizontal_alignment="center"),
        margin=ft.margin.only(top=40, bottom=30)
    )

    dob_input = ft.TextField(
        label="Дата рождения",
        hint_text="ДД.ММ.ГГГГ",
        border_color=PRIMARY_COLOR,
        focused_border_color=SECONDARY_COLOR,
        color="white",
        width=300,
        text_align="center"
    )

    calc_button = ft.ElevatedButton(
        text="РАССЧИТАТЬ СУДЬБУ",
        on_click=calculate_click,
        style=ft.ButtonStyle(
            color="white",
            bgcolor=PRIMARY_COLOR,
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        width=300
    )

    results_column = ft.Column(scroll="auto", expand=True)

    # Layout
    page.add(
        ft.Column([
            header,
            ft.Container(content=dob_input, alignment=ft.alignment.center),
            ft.Container(content=calc_button, alignment=ft.alignment.center, margin=ft.margin.only(top=10)),
            results_column
        ], horizontal_alignment="center", expand=True)
    )

if __name__ == "__main__":
    print("--- ЗАПУСК ПРИЛОЖЕНИЯ AI NOMEROLOGY ---")
    print("Если окно не открылось само, скопируйте этот адрес в браузер: http://127.0.0.1:8550")
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8550)
