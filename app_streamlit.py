import streamlit as st
import datetime
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from numerology_logic import NumerologyCalculator as calc

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(
    page_title="AI Nomerology Pro",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- СТИЛИЗАЦИЯ И ТЕМЫ ---
st.markdown("""
    <style>
    /* Основной фон */
    .stApp {
        background: radial-gradient(circle at top right, #1E1E3F, #0F0F1F);
        color: #E0E0E0;
    }
    
    /* Неоновый текст */
    .neon-text {
        text-shadow: 0 0 10px #7B61FF, 0 0 20px #7B61FF;
        color: white;
        font-weight: bold;
    }
    
    /* Стеклянные карточки */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 24px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(15px);
        margin-bottom: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    /* Индикатор удачи */
    .luck-pill {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        text-transform: uppercase;
        margin-right: 10px;
    }
    
    /* Сетка Ло Шу */
    .loshu-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        max-width: 320px;
        margin: 25px auto;
    }
    .loshu-cell {
        aspect-ratio: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: rgba(123, 97, 255, 0.15);
        border: 1px solid rgba(123, 97, 255, 0.5);
        border-radius: 16px;
        font-size: 26px;
        font-weight: 800;
        color: #FFD700;
        transition: 0.3s;
    }
    .loshu-cell:hover {
        background: rgba(123, 97, 255, 0.3);
        transform: scale(1.05);
    }
    
    /* Боковое меню */
    [data-testid="stSidebar"] {
        background-color: #0A0A1A;
        border-right: 1px solid rgba(123, 97, 255, 0.2);
    }
    
    /* Кнопки */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #7B61FF 0%, #B485FF 100%);
        color: white;
        border: none;
        border-radius: 16px;
        padding: 20px;
        font-size: 18px;
        font-weight: 600;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(123, 97, 255, 0.3);
    }
    
    /* Рекламный баннер */
    .ad-banner-style {
        background: #000;
        border: 1px solid #222;
        padding: 10px;
        text-align: center;
        border-radius: 10px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---
def get_energy_chart(dob):
    days = [datetime.date.today() + datetime.timedelta(days=i) for i in range(30)]
    seed = sum(int(d) for d in dob if d.isdigit())
    values = [50 + 40 * np.sin((seed + i) * 0.3) for i in range(30)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=days, y=values,
        mode='lines',
        line=dict(color='#7B61FF', width=4),
        fill='toself',
        fillcolor='rgba(123, 97, 255, 0.1)',
        name="Энергия"
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=20, b=0),
        height=250,
        xaxis=dict(showgrid=False, tickfont=dict(color="gray")),
        yaxis=dict(showgrid=False, range=[0, 100], visible=False),
        showlegend=False
    )
    return fig

# --- БОКОВАЯ ПАНЕЛЬ ---
with st.sidebar:
    st.markdown("<h2 class='neon-text'>AI NOMEROLOGY</h2>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio(
        "Разделы",
        ["🏠 Главная", "📈 Пульс Энергии", "🏮 Квадрат Ло Шу", "💞 Совместимость Душ", "📚 Книга Судьбы (PDF)"]
    )
    st.markdown("---")
    st.markdown("💸 **Доход от рекламы:** `$1.24` (Демо)")
    st.info("Версия 1.0.1 (Android Ready)")

# --- ОСНОВНОЙ КОНТЕНТ ---

if menu == "🏠 Главная":
    st.markdown("<h1>Ваш Цифровой Код</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        dob = st.text_input("Введите дату рождения", placeholder="20.10.1990")
        btn = st.button("РАССЧИТАТЬ СУДЬБУ")
        st.markdown('</div>', unsafe_allow_html=True)

        if dob:
            try:
                datetime.datetime.strptime(dob, "%d.%m.%Y")
                lp = calc.calculate_life_path(dob)['value']
                vedic = calc.get_vedic_numbers(dob)
                
                st.markdown(f"""
                    <div class="glass-card">
                        <div style="display: flex; justify-content: space-between;">
                            <span class="luck-pill" style="background: #2ECC71; color: #FFF;">Статус: Высокая энергия</span>
                            <span style="color: #FFD700; font-weight: bold;">Число ЖП: {lp}</span>
                        </div>
                        <h2 style="margin-top: 15px;">Ваша Вибрация</h2>
                        <p style="font-size: 1.1em; line-height: 1.6;">{calc.get_interpretation(lp)}</p>
                    </div>
                """, unsafe_allow_html=True)
            except:
                st.error("Неверный формат даты")

    with col2:
        st.markdown("### Прогноз Энергии")
        if dob:
            st.plotly_chart(get_energy_chart(dob), use_container_width=True)
            st.info(calc.get_daily_insight(dob))
        else:
            st.write("Введите дату для прогноза.")

elif menu == "📈 Пульс Энергии":
    st.markdown("<h1>Анализ Биоритмов</h1>", unsafe_allow_html=True)
    st.write("Глубокий анализ ваших физических и кармических циклов на ближайшие 30 дней.")
    
    dob = st.text_input("Введите дату", key="pulse_dob")
    if dob:
        st.plotly_chart(get_energy_chart(dob), use_container_width=True)
        st.markdown("""
            <div class="glass-card">
                <h4>Важные инсайты:</h4>
                <ul>
                    <li><b>Физический цикл:</b> Период пиковой активности.</li>
                    <li><b>Ментальный цикл:</b> Интуиция обострена.</li>
                    <li><b>Финансы:</b> Избегайте крупных трат на этой неделе.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

elif menu == "🏮 Квадрат Ло Шу":
    st.markdown("<h1>Древнекитайская Матрица</h1>", unsafe_allow_html=True)
    st.write("Баланс 5 стихий в вашей дате рождения.")
    dob = st.text_input("Дата рождения для матрицы", key="loshu_dob")
    
    if dob:
        grid = calc.get_chinese_lo_shu(dob)
        flat_grid = [grid[0][0], grid[0][1], grid[0][2], 
                     grid[1][0], grid[1][1], grid[1][2], 
                     grid[2][0], grid[2][1], grid[2][2]]
        
        elements = ["Дерево", "Огонь", "Земля", "Дерево", "Земля", "Металл", "Земля", "Вода", "Металл"]
        
        st.markdown('<div class="loshu-container">', unsafe_allow_html=True)
        for i, val in enumerate(flat_grid):
            display_val = val if val != 0 else ""
            st.markdown(f'<div class="loshu-cell"><div>{display_val}</div><div style="font-size: 8px; color: #7B61FF;">{elements[i]}</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif menu == "💞 Совместимость Душ":
    st.markdown("<h1>Резонанс и Гармония</h1>", unsafe_allow_html=True)
    st.write("Проверьте, насколько ваши цифровые коды гармонируют друг с другом.")
    d1 = st.text_input("Ваша дата", placeholder="ДД.ММ.ГГГГ")
    d2 = st.text_input("Дата партнера", placeholder="ДД.ММ.ГГГГ")
    
    if st.button("СИНХРОНИЗИРОВАТЬ ДУШИ") and d1 and d2:
        report = calc.get_compatibility_report(d1, d2)
        st.markdown(f'<div class="glass-card">{report}</div>', unsafe_allow_html=True)

elif menu == "📚 Книга Судьбы (PDF)":
    st.markdown("<h1 class='neon-text'>Ваша Персональная Книга</h1>", unsafe_allow_html=True)
    st.markdown("""
        <div class="glass-card" style="border: 1px solid #FFD700;">
            <h3 style="color: #FFD700 !important;">Раскройте свой полный потенциал</h3>
            <p>Сгенерируйте 30-страничный PDF-отчет, включающий:</p>
            <ul>
                <li>Глубокий разбор Жизненного Пути</li>
                <li>Кармические долги и уроки</li>
                <li>Циклы года, месяца и дня</li>
                <li>Совместимость в 5 ключевых сферах</li>
            </ul>
            <center><button style="background: gold; color: black; border: none; padding: 15px 30px; border-radius: 10px; font-weight: bold; width: 100%;">ПОЛУЧИТЬ ЗА 445₽</button></center>
        </div>
    """, unsafe_allow_html=True)

# РЕКЛАМНЫЙ БАННЕР ВНИЗУ
st.markdown("""
    <div class="ad-banner-style">
        <small style="color: #555;">РЕКЛАМА от Google AdMob</small><br>
        <b style="color: #7B61FF;">Найди свою половинку с AI Astrology</b>
    </div>
""", unsafe_allow_html=True)
