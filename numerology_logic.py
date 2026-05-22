import datetime
from typing import Dict, Any, List, Tuple

class NumerologyCalculator:
    # Systems configuration
    PYTHAGOREAN_MAP = {
        'а': 1, 'б': 2, 'в': 3, 'г': 4, 'д': 5, 'е': 6, 'ё': 7, 'ж': 8, 'з': 9,
        'и': 1, 'й': 2, 'к': 3, 'л': 4, 'м': 5, 'н': 6, 'о': 7, 'п': 8, 'р': 9,
        'с': 1, 'т': 2, 'у': 3, 'ф': 4, 'х': 5, 'ц': 6, 'ч': 7, 'ш': 8, 'щ': 9,
        'ъ': 1, 'ы': 2, 'ь': 3, 'э': 4, 'ю': 5, 'я': 6
    }
    
    CHALDEAN_MAP = {
        'а': 1, 'б': 2, 'в': 6, 'г': 3, 'д': 4, 'е': 5, 'ё': 5, 'ж': 4, 'з': 7,
        'и': 1, 'й': 1, 'к': 2, 'л': 3, 'м': 4, 'н': 5, 'о': 7, 'п': 8, 'р': 2,
        'с': 3, 'т': 4, 'у': 6, 'ф': 8, 'х': 5, 'ц': 3, 'ч': 8, 'ш': 2, 'щ': 2,
        'ъ': 0, 'ы': 1, 'ь': 0, 'э': 5, 'ю': 7, 'я': 2
    }

    VOWELS = "аеёиоуэюя"

    MASTER_NUMBERS = [11, 22, 33, 44]
    KARMIC_DEBTS = [13, 14, 16, 19]

    @staticmethod
    def reduce_number(n: int, master: bool = True) -> int:
        if master and n in NumerologyCalculator.MASTER_NUMBERS:
            return n
        while n > 9:
            if master and n in NumerologyCalculator.MASTER_NUMBERS:
                return n
            n = sum(int(d) for d in str(n))
        return n

    @classmethod
    def calculate_life_path(cls, dob: str) -> Dict[str, Any]:
        """
        Calculates Life Path Number and checks for Master Numbers and Karmic Debts.
        dob format: DD.MM.YYYY
        """
        d, m, y = map(int, dob.split('.'))
        
        # Method: Reduce each part, then sum, then reduce again
        r_d = cls.reduce_number(d, master=False)
        r_m = cls.reduce_number(m, master=False)
        r_y = cls.reduce_number(y, master=False)
        
        total = r_d + r_m + r_y
        final_lp = cls.reduce_number(total, master=True)
        
        # Check for karmic debt in intermediate steps
        debts = [debt for debt in cls.KARMIC_DEBTS if debt == total]
        
        return {
            "value": final_lp,
            "is_master": final_lp in cls.MASTER_NUMBERS,
            "karmic_debts": debts,
            "raw_sum": total
        }

    @classmethod
    def calculate_destiny_soul_personality(cls, name: str, system: str = "pythagorean") -> Dict[str, int]:
        name = name.lower().replace(" ", "")
        mapping = cls.PYTHAGOREAN_MAP if system == "pythagorean" else cls.CHALDEAN_MAP
        
        all_vals = [mapping.get(c, 0) for c in name if c.isalpha()]
        destiny = cls.reduce_number(sum(all_vals))
        
        vowel_vals = [mapping.get(c, 0) for c in name if c in cls.VOWELS and c.isalpha()]
        soul_urge = cls.reduce_number(sum(vowel_vals))
        
        consonant_vals = [mapping.get(c, 0) for c in name if c not in cls.VOWELS and c.isalpha()]
        personality = cls.reduce_number(sum(consonant_vals))
        
        return {
            "destiny": destiny,
            "soul_urge": soul_urge,
            "personality": personality
        }

    @classmethod
    def get_vedic_numbers(cls, dob: str) -> Dict[str, int]:
        """
        Vedic numerology (Sankhya Shastra): 
        Psychic Number (Day of birth)
        Destiny Number (Full date)
        """
        d, m, y = map(int, dob.split('.'))
        psychic = cls.reduce_number(d, master=False)
        
        total = sum(int(digit) for digit in dob if digit.isdigit())
        destiny = cls.reduce_number(total, master=False)
        
        return {
            "psychic": psychic,
            "destiny": destiny
        }

    @classmethod
    def get_chinese_lo_shu(cls, dob: str) -> List[List[int]]:
        """
        Returns Lo Shu Square (3x3 grid)
        4 9 2
        3 5 7
        8 1 6
        """
        digits = [int(d) for d in dob if d.isdigit()]
        grid = [
            [4 if 4 in digits else 0, 9 if 9 in digits else 0, 2 if 2 in digits else 0],
            [3 if 3 in digits else 0, 5 if 5 in digits else 0, 7 if 7 in digits else 0],
            [8 if 8 in digits else 0, 1 if 1 in digits else 0, 6 if 6 in digits else 0]
        ]
        return grid

    @staticmethod
    def get_interpretation(lp: int) -> str:
        interpretations = {
            1: "<b>Число 1: Лидер, Первопроходец.</b>\nТы здесь, чтобы прокладывать новые пути. Твоя сила в независимости. Теневая сторона: эгоцентризм и нетерпимость. Линда Гудман говорила, что Единицы — это дети Зодиака, всегда требующие внимания к своим идеям.",
            2: "<b>Число 2: Дипломат, Миротворец.</b>\nТвое оружие — интуиция и мягкая сила. Ты мастер партнерства. Тень: чрезмерная чувствительность и зависимость от мнения окружающих. Хайро считал, что Двойки черпают силу в тени, управляя процессами незаметно.",
            3: "<b>Число 3: Творец, Коммуникатор.</b>\nЖизнь для тебя — сцена. Твой дар — самовыражение. Тень: разбросанность и поверхностность. Мэтью Оливер называл Тройку 'числом радости', которое часто забывает о дисциплине.",
            4: "<b>Число 4: Строитель, Прагматик.</b>\nПорядок, система, фундамент. На тебя можно положиться. Тень: жесткость, упрямство, страх перемен. В ведической нумерологии 4 — это Раху, энергия, дающая материальный успех через тяжелый труд.",
            5: "<b>Число 5: Искатель Свободы, Авантюрист.</b>\nПеремены — твой кислород. Ты мастер адаптации. Тень: безответственность и потакание слабостям. Линда Гудман предупреждала Пятерок о риске потерять себя в бесконечной погоне за новизной.",
            6: "<b>Число 6: Наставник, Опекун.</b>\nОтветственность и гармония. Твой дом — твоя крепость. Тень: вмешательство в чужую жизнь под видом 'заботы'. Шестерки часто несут на себе груз всей семьи.",
            7: "<b>Число 7: Мистик, Аналитик.</b>\nПоиск истины в глубине. Тебе нужно одиночество для познания. Тень: замкнутость, цинизм, отрыв от реальности. Хайро называл Семерку самым философским числом.",
            8: "<b>Число 8: Властелин, Капиталист.</b>\nДеньги и власть — твои инструменты. Ты понимаешь законы кармы и баланса. Тень: жадность, тирания. Это число больших достижений и больших потерь.",
            9: "<b>Число 9: Гуманист, Завершитель.</b>\nТы здесь, чтобы служить человечеству. Твой опыт огромен. Тень: драматизм и жизнь в прошлом. Девятка — это итог всех чисел, символ мудрости.",
            11: "<b>Мастер-число 11: Просветленный.</b>\nКанал между мирами. Сверхчувствительность. Твой путь труден, так как ты чувствуешь больше, чем другие. Хайро называл 11 числом мученичества или великого триумфа.",
            22: "<b>Мастер-число 22: Мастер-Строитель.</b>\nСпособность воплощать самые грандиозные мечты в реальность. Ты строишь для вечности. Огромная ответственность.",
            33: "<b>Мастер-число 33: Мастер-Учитель.</b>\nСамоотверженная любовь и служение. Уровень Христа. Редкий дар исцеления словом.",
            44: "<b>Мастер-число 44: Мастер Созидания.</b>\nУровень мирового влияния и материализации высших смыслов. Стальная воля."
        }
        return interpretations.get(lp, "Загадочное число с неопределенной судьбой.")

    @staticmethod
    def get_karmic_debt_text(debt: int) -> str:
        texts = {
            13: "<b>Кармический долг 13: Труд.</b> В прошлом ты избегал ответственности. Теперь успех придет только через дисциплину и упорство.",
            14: "<b>Кармический долг 14: Злоупотребление свободой.</b> Прошлые жизни были полны излишеств. Сейчас важно найти баланс и не впадать в зависимости.",
            16: "<b>Кармический долг 16: Гордыня.</b> Разрушение эго. Тебе предстоит научиться смирению через внезапные перемены.",
            19: "<b>Кармический долг 19: Злоупотребление властью.</b> Ты игнорировал других. Теперь тебе придется научиться просить о помощи и учитывать интересы окружающих."
        }
        return texts.get(debt, "")

    @classmethod
    def get_daily_insight(cls, dob: str) -> str:
        """Calculates Personal Day and returns a mystical insight."""
        d, m, _ = map(int, dob.split('.'))
        now = datetime.datetime.now()
        
        # Personal Year = Day + Month + Current Year
        py = cls.reduce_number(cls.reduce_number(d, False) + cls.reduce_number(m, False) + cls.reduce_number(now.year, False))
        # Personal Month = Personal Year + Current Month
        pm = cls.reduce_number(py + cls.reduce_number(now.month, False))
        # Personal Day = Personal Month + Current Day
        pd = cls.reduce_number(pm + cls.reduce_number(now.day, False))
        
        insights = {
            1: "День начинаний. Энергия Солнца дает тебе мощный импульс. Не бойся сделать первый шаг в том, что давно откладывал.",
            2: "День партнерства. Слушай других, но не теряй себя. Интуиция сегодня сильнее логики. Мягкость — твое оружие.",
            3: "День творчества и радости. Слово сегодня имеет магическую силу. Делись идеями, свети и вдохновляй окружающих.",
            4: "День порядка. Хорошее время для планирования и укрепления фундамента. Дисциплина принесет плоды.",
            5: "День перемен. Будь готов к неожиданностям. Свобода выбора сегодня в твоих руках. Избегай излишеств.",
            6: "День гармонии и семьи. Прояви заботу о близких. Твое тепло сегодня способно исцелять старые раны.",
            7: "День тишины. Погрузись в себя. Ответы придут не извне, а из глубины твоего подсознания. Время для анализа.",
            8: "День силы. Направь энергию на материальные достижения. Справедливость и баланс — твои ориентиры сегодня.",
            9: "День завершения. Отпусти то, что больше не служит тебе. Очисти пространство для нового цикла. Прощай и отпускай."
        }
        
        text = insights.get(pd, "Числа сегодня шепчут о неопределенности. Будь внимателен к знакам.")
        return f"✨ <b>ПЕРСОНАЛЬНЫЙ СОВЕТ НА СЕГОДНЯ</b>\n\nТвоё число дня: <b>{pd}</b>\n\n{text}"

    @classmethod
    def get_compatibility_report(cls, dob1: str, dob2: str) -> str:
        """Analyzes compatibility between two dates of birth."""
        lp1 = cls.calculate_life_path(dob1)['value']
        lp2 = cls.calculate_life_path(dob2)['value']
        
        # Simple mystical logic for compatibility
        score = 100 - abs(lp1 - lp2) * 10
        if lp1 == lp2: score = 95 # Same numbers - high resonance but can be boring
        if (lp1 + lp2) in [11, 22, 33]: score = 99 # Master resonance
        
        analysis = ""
        if score > 80:
            analysis = "Ваши души вибрируют на схожих частотах. Это союз, где понимание происходит без слов, а кармические задачи дополняют друг друга."
        elif score > 50:
            analysis = "Это союз испытаний и роста. Вам придется многому научиться друг у друга, но именно в этом трении рождается истинный свет."
        else:
            analysis = "Ваши пути пересекаются под острым углом. Это яркая, но сложная связь, требующая огромного смирения и работы над эго."
            
        report = (
            f"💞 <b>АНАЛИЗ СОВМЕСТИМОСТИ</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"👤 Партнер 1 (ЧЖП {lp1})\n"
            f"👤 Партнер 2 (ЧЖП {lp2})\n\n"
            f"📊 <b>Резонанс Душ: {score}%</b>\n\n"
            f"🔮 <b>Вердикт Numeros:</b>\n{analysis}\n\n"
            f"<i>Совет: {'Ищите общие цели и не бойтесь глубины.' if score > 70 else 'Будьте терпеливы к теням друг друга.'}</i>\n"
            f"━━━━━━━━━━━━━━━━━━━━"
        )
        return report

    @classmethod
    def get_full_report(cls, dob: str, name: str) -> str:
        """Generates a comprehensive 12+ parameter report."""
        lp_data = cls.calculate_life_path(dob)
        lp = lp_data['value']
        vedic = cls.get_vedic_numbers(dob)
        name_nums = cls.calculate_destiny_soul_personality(name)
        
        # Calculate cycles (simplified logic for demonstration)
        d, m, y = map(int, dob.split('.'))
        personal_year = cls.reduce_number(cls.reduce_number(d, False) + cls.reduce_number(m, False) + cls.reduce_number(datetime.datetime.now().year, False))
        
        report = (
            f"📜 <b>ПОЛНЫЙ НУМЕРОЛОГИЧЕСКИЙ ПАСПОРТ: {name}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"💎 <b>1. ОСНОВНЫЕ ЧИСЛА</b>\n"
            f"• Число Жизненного Пути: <b>{lp}</b> — Глобальная цель воплощения.\n"
            f"• Число Судьбы (Имя): <b>{name_nums['destiny']}</b> — Твои таланты и инструменты.\n"
            f"• Число Души (Сердца): <b>{name_nums['soul_urge']}</b> — Твои скрытые желания.\n"
            f"• Число Личности (Внешнее): <b>{name_nums['personality']}</b> — Как тебя видят другие.\n\n"
            
            f"🕉 <b>2. ВЕДИЧЕСКИЙ АНАЛИЗ</b>\n"
            f"• Число Души (День): <b>{vedic['psychic']}</b> — Твой характер до 35 лет.\n"
            f"• Число Кармы (Вся дата): <b>{vedic['destiny']}</b> — Влияние планет на твой путь.\n\n"
            
            f"🔮 <b>3. КАРМИЧЕСКИЕ ПАРАМЕТРЫ</b>\n"
            f"• Долги: {', '.join(map(str, lp_data['karmic_debts'])) if lp_data['karmic_debts'] else 'Отсутствуют'}\n"
            f"• Мастер-вибрации: {'Да' if lp_data['is_master'] else 'Нет'}\n\n"
            
            f"⏳ <b>4. ЦИКЛЫ И ПРОГНОЗ</b>\n"
            f"• Текущий персональный год: <b>{personal_year}</b>\n"
            f"<i>Инсайт: {'Время для новых начинаний' if personal_year == 1 else 'Время для завершения и очистки' if personal_year == 9 else 'Период активного роста и обучения'}.</i>\n\n"
            
            f"🛡 <b>5. ВЫЗОВЫ И УРОКИ</b>\n"
            f"Твой главный вызов — научиться балансировать между {'эго и служением' if lp % 2 == 0 else 'материальным и духовным'}.\n\n"
            
            f"📍 <b>6. ГЛУБОКИЙ СИНТЕЗ</b>\n"
            f"{cls.get_interpretation(lp)}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"<i>Это твой путеводитель. Используй его мудро.</i>"
        )
        return report
