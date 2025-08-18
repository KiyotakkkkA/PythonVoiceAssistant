from typing import Optional, List, Tuple, Set
from functools import lru_cache
from interfaces import IService
import re


class TextToNumberService(IService):
    SERVICE_NAME = "TextToNumberService"

    DIGITS = {
        'ноль': 0, 'один': 1, 'одна': 1, 'два': 2, 'две': 2, 'три': 3,
        'четыре': 4, 'пять': 5, 'шесть': 6, 'семь': 7, 'восемь': 8, 'девять': 9
    }

    TEENS = {
        'десять': 10, 'одиннадцать': 11, 'двенадцать': 12, 'тринадцать': 13,
        'четырнадцать': 14, 'пятнадцать': 15, 'шестнадцать': 16,
        'семнадцать': 17, 'восемнадцать': 18, 'девятнадцать': 19
    }

    TENS = {
        'двадцать': 20, 'тридцать': 30, 'сорок': 40, 'пятьдесят': 50,
        'шестьдесят': 60, 'семьдесят': 70, 'восемьдесят': 80, 'девяносто': 90
    }

    HUNDREDS = {
        'сто': 100, 'двести': 200, 'триста': 300, 'четыреста': 400,
        'пятьсот': 500, 'шестьсот': 600, 'семьсот': 700,
        'восемьсот': 800, 'девятьсот': 900
    }

    SCALE_WORDS = {
        'тысяча': 1000, 'тысячи': 1000, 'тысяч': 1000,
        'миллион': 1000000, 'миллиона': 1000000, 'миллионов': 1000000,
        'миллиард': 1000000000, 'миллиарда': 1000000000, 'миллиардов': 1000000000
    }

    ORDINAL_BASES = {
        'первый': 1, 'первая': 1, 'первое': 1, 'первые': 1, 'первого': 1, 'первой': 1, 'первому': 1, 'первым': 1,
        'второй': 2, 'вторая': 2, 'второе': 2, 'вторые': 2, 'второго': 2, 'второй': 2, 'второму': 2, 'вторым': 2,
        'третий': 3, 'третья': 3, 'третье': 3, 'третьи': 3, 'третьего': 3, 'третьей': 3, 'третьему': 3, 'третьим': 3,
        'четвёртый': 4, 'четвёртая': 4, 'четвёртое': 4, 'четвёртые': 4, 'четвёртого': 4, 'четвёртой': 4, 'четвёртому': 4, 'четвёртым': 4,
        'пятый': 5, 'пятая': 5, 'пятое': 5, 'пятые': 5, 'пятого': 5, 'пятой': 5, 'пятому': 5, 'пятым': 5,
        'шестой': 6, 'шестая': 6, 'шестое': 6, 'шестые': 6, 'шестого': 6, 'шестой': 6, 'шестому': 6, 'шестым': 6,
        'седьмой': 7, 'седьмая': 7, 'седьмое': 7, 'седьмые': 7, 'седьмого': 7, 'седьмой': 7, 'седьмому': 7, 'седьмым': 7,
        'восьмой': 8, 'восьмая': 8, 'восьмое': 8, 'восьмые': 8, 'восьмого': 8, 'восьмой': 8, 'восьмому': 8, 'восьмым': 8,
        'девятый': 9, 'девятая': 9, 'девятое': 9, 'девятые': 9, 'девятого': 9, 'девятой': 9, 'девятому': 9, 'девятым': 9,

        'десятый': 10, 'десятая': 10, 'десятое': 10, 'десятые': 10,
        'одиннадцатый': 11, 'одиннадцатая': 11, 'одиннадцатое': 11, 'одиннадцатые': 11,
        'двенадцатый': 12, 'двенадцатая': 12, 'двенадцатое': 12, 'двенадцатые': 12,
        'тринадцатый': 13, 'тринадцатая': 13, 'тринадцатое': 13, 'тринадцатые': 13,
        'четырнадцатый': 14, 'четырнадцатая': 14, 'четырнадцатое': 14, 'четырнадцатые': 14,
        'пятнадцатый': 15, 'пятнадцатая': 15, 'пятнадцатое': 15, 'пятнадцатые': 15,
        'шестнадцатый': 16, 'шестнадцатая': 16, 'шестнадцатое': 16, 'шестнадцатые': 16,
        'семнадцатый': 17, 'семнадцатая': 17, 'семнадцатое': 17, 'семнадцатые': 17,
        'восемнадцатый': 18, 'восемнадцатая': 18, 'восемнадцатое': 18, 'восемнадцатые': 18,
        'девятнадцатый': 19, 'девятнадцатая': 19, 'девятнадцатое': 19, 'девятнадцатые': 19,

        'двадцатый': 20, 'двадцатая': 20, 'двадцатое': 20, 'двадцатые': 20,
        'двадцатого': 20, 'двадцатой': 20, 'двадцатому': 20, 'двадцатым': 20,
        'тридцатый': 30, 'тридцатая': 30, 'тридцатое': 30, 'тридцатые': 30,
        'тридцатого': 30, 'тридцатой': 30, 'тридцатому': 30, 'тридцатым': 30,
        'сороковой': 40, 'сороковая': 40, 'сороковое': 40, 'сороковые': 40,
        'сорокового': 40, 'сороковой': 40, 'сороковому': 40, 'сороковым': 40,
        'пятидесятый': 50, 'пятидесятая': 50, 'пятидесятое': 50, 'пятидесятые': 50,
        'пятидесятого': 50, 'пятидесятой': 50, 'пятидесятому': 50, 'пятидесятым': 50,
        'шестидесятый': 60, 'шестидесятая': 60, 'шестидесятое': 60, 'шестидесятые': 60,
        'шестидесятого': 60, 'шестидесятой': 60, 'шестидесятому': 60, 'шестидесятым': 60,
        'семидесятый': 70, 'семидесятая': 70, 'семидесятое': 70, 'семидесятые': 70,
        'семидесятого': 70, 'семидесятой': 70, 'семидесятому': 70, 'семидесятым': 70,
        'восьмидесятый': 80, 'восьмидесятая': 80, 'восьмидесятое': 80, 'восьмидесятые': 80,
        'восьмидесятого': 80, 'восьмидесятой': 80, 'восьмидесятому': 80, 'восьмидесятым': 80,
        'девяностый': 90, 'девяностая': 90, 'девяностое': 90, 'девяностые': 90,
        'девяностого': 90, 'девяностой': 90, 'девяностому': 90, 'девяностым': 90,

        'сотый': 100, 'сотая': 100, 'сотое': 100, 'сотые': 100,
        'сотого': 100, 'сотой': 100, 'сотому': 100, 'сотым': 100,
        'двухсотый': 200, 'двухсотая': 200, 'двухсотое': 200, 'двухсотые': 200,
        'двухсотого': 200, 'двухсотой': 200, 'двухсотому': 200, 'двухсотым': 200,
        'трёхсотый': 300, 'трёхсотая': 300, 'трёхсотое': 300, 'трёхсотые': 300,
        'трёхсотого': 300, 'трёхсотой': 300, 'трёхсотому': 300, 'трёхсотым': 300,
        'четырёхсотый': 400, 'четырёхсотая': 400, 'четырёхсотое': 400, 'четырёхсотые': 400,
        'четырёхсотого': 400, 'четырёхсотой': 400, 'четырёхсотому': 400, 'четырёхсотым': 400,
        'пятисотый': 500, 'пятисотая': 500, 'пятисотое': 500, 'пятисотые': 500,
        'пятисотого': 500, 'пятисотой': 500, 'пятисотому': 500, 'пятисотым': 500,
        'шестисотый': 600, 'шестисотая': 600, 'шестисотое': 600, 'шестисотые': 600,
        'шестисотого': 600, 'шестисотой': 600, 'шестисотому': 600, 'шестисотым': 600,
        'семисотый': 700, 'семисотая': 700, 'семисотое': 700, 'семисотые': 700,
        'семисотого': 700, 'семисотой': 700, 'семисотому': 700, 'семисотым': 700,
        'восьмисотый': 800, 'восьмисотая': 800, 'восьмисотое': 800, 'восьмисотые': 800,
        'восьмисотого': 800, 'восьмисотой': 800, 'восьмисотому': 800, 'восьмисотым': 800,
        'девятисотый': 900, 'девятисотая': 900, 'девятисотое': 900, 'девятисотые': 900,
        'девятисотого': 900, 'девятисотой': 900, 'девятисотому': 900, 'девятисотым': 900,

        'тысячный': 1000, 'тысячная': 1000, 'тысячное': 1000, 'тысячные': 1000,
        'тысячного': 1000, 'тысячной': 1000, 'тысячному': 1000, 'тысячным': 1000,
        'миллионный': 1000000, 'миллионная': 1000000, 'миллионное': 1000000, 'миллионные': 1000000,
        'миллионного': 1000000, 'миллионной': 1000000, 'миллионному': 1000000, 'миллионным': 1000000,
        'миллиардный': 1000000000, 'миллиардная': 1000000000, 'миллиардное': 1000000000, 'миллиардные': 1000000000,
        'миллиардного': 1000000000, 'миллиардной': 1000000000, 'миллиардному': 1000000000, 'миллиардным': 1000000000,
    }

    ORDINAL_SUFFIXES = [
        ('ый', ''), ('ой', ''), ('ая', ''), ('ое', ''), ('ые', ''), ('ых', ''), ('ым', ''),
        ('его', 'ой'), ('ем', 'ом'), ('ому', 'ому'), ('ей', 'ей'), ('ими', 'ими'), ('ых', 'ых'),
    ]

    ALL_NUMBER_WORDS: Set[str] = (
        set(DIGITS) | set(TEENS) | set(TENS) | set(HUNDREDS) |
        set(SCALE_WORDS) | set(ORDINAL_BASES)
    )

    @classmethod
    def _is_number_word(cls, word: str) -> bool:
        word = word.lower()
        if word in cls.ALL_NUMBER_WORDS:
            return True
        return cls._normalize_ordinal(word) is not None

    @classmethod
    def _normalize_ordinal(cls, word: str) -> Optional[int]:
        word = word.lower().strip()
        if word in cls.ORDINAL_BASES:
            return cls.ORDINAL_BASES[word]

        for suffix, replacement in cls.ORDINAL_SUFFIXES:
            if word.endswith(suffix):
                base = word[:-len(suffix)] + replacement
                mapping = {
                    'двадцат': 'двадцать', 'тридцат': 'тридцать', 'сороков': 'сорок',
                    'пятидесят': 'пятьдесят', 'шестидесят': 'шестьдесят',
                    'семидесят': 'семьдесят', 'восьмидесят': 'восемьдесят', 'девяност': 'девяносто',
                    'сот': 'сто', 'двухсот': 'двести', 'трёхсот': 'триста',
                    'четырёхсот': 'четыреста', 'пятисот': 'пятьсот', 'шестисот': 'шестьсот',
                    'семисот': 'семьсот', 'восьмисот': 'восемьсот', 'девятисот': 'девятьсот',
                    'тысяч': 'тысяча', 'миллион': 'миллион', 'миллиард': 'миллиард'
                }
                if base in mapping:
                    try:
                        return cls._get_value_from_known_word(mapping[base])
                    except KeyError:
                        pass
                if base == 'перв': return 1
                if base == 'втор': return 2
                if base == 'трет': return 3
                if base == 'четверт': return 4
        return None

    @classmethod
    def _get_value_from_known_word(cls, word: str) -> int:
        if word in cls.DIGITS: return cls.DIGITS[word]
        if word in cls.TEENS: return cls.TEENS[word]
        if word in cls.TENS: return cls.TENS[word]
        if word in cls.HUNDREDS: return cls.HUNDREDS[word]
        if word in cls.SCALE_WORDS: return cls.SCALE_WORDS[word]
        if word in cls.ORDINAL_BASES: return cls.ORDINAL_BASES[word]
        raise KeyError(word)

    @classmethod
    @lru_cache(maxsize=1024)
    def text_to_number(cls, text: str) -> Optional[int]:
        if not text or not text.strip():
            return None
        words = text.lower().split()
        if not any(cls._is_number_word(word) for word in words):
            return None
        try:
            return cls._parse_number_sequence(words)
        except Exception:
            return None

    @classmethod
    def _parse_number_sequence(cls, words: List[str]) -> int:
        result = 0
        current_group = 0
        i = 0
        while i < len(words):
            word = words[i].lower()
            try:
                value = cls._get_word_value(word)
            except ValueError:
                i += 1
                continue

            if word in cls.SCALE_WORDS:
                multiplier = cls.SCALE_WORDS[word]
                if current_group == 0:
                    current_group = 1
                result += current_group * multiplier
                current_group = 0
            else:
                current_group += value
            i += 1
        return result + current_group

    @classmethod
    def _get_word_value(cls, word: str) -> int:
        word = word.lower()
        if word in cls.ALL_NUMBER_WORDS:
            return cls._get_value_from_known_word(word)
        ordinal = cls._normalize_ordinal(word)
        if ordinal is not None:
            return ordinal
        raise ValueError(f"Неизвестное числовое слово: {word}")

    @classmethod
    def execute(cls, text: str) -> str:
        if not text or not text.strip():
            return text

        tokens = re.findall(r'\S+|\s+', text)
        word_positions = [(i, token.lower()) for i, token in enumerate(tokens) if not token.isspace()]
        replacements = cls._find_number_sequences(word_positions)

        result_tokens = tokens.copy()
        for start, end, number in sorted(replacements, reverse=True):
            result_tokens[start:end + 1] = [f"{number}"]

        return ''.join(result_tokens)

    @classmethod
    def _find_number_sequences(cls, word_positions: List[Tuple[int, str]]) -> List[Tuple[int, int, int]]:
        replacements = []
        used_positions = set()
        i = 0

        while i < len(word_positions):
            if i in used_positions:
                i += 1
                continue

            current_words = []
            current_indices = []
            best_number = None
            best_end_idx = None

            j = i
            while j < len(word_positions) and j not in used_positions:
                word = word_positions[j][1]
                if not cls._is_number_word(word):
                    break

                current_words.append(word)
                current_indices.append(j)
                phrase = ' '.join(current_words)

                number = cls.text_to_number(phrase)
                if number is not None:
                    best_number = number
                    best_end_idx = j

                j += 1

            if best_number is not None:
                start_token = word_positions[i][0]
                end_token = word_positions[best_end_idx][0]
                replacements.append((start_token, end_token, best_number))
                used_positions.update(current_indices[:best_end_idx - i + 1])
                i = best_end_idx + 1
            else:
                i += 1

        return replacements

    @classmethod
    def test(cls, console_output: bool = False):
        test_cases = [
            {'input': "привет сто двадцать пять потом проверка двадцать семь", 'output': "привет 125 потом проверка 27"},
            {'input': "у меня есть три кота и пять собак", 'output': "у меня есть 3 кота и 5 собак"},
            {'input': "стоимость составляет две тысячи триста рублей", 'output': "стоимость составляет 2300 рублей"},
            {'input': "один два три четыре", 'output': "10"},
            {'input': "обычный текст без чисел", 'output': "обычный текст без чисел"},
            {'input': "сто", 'output': "100"},
            {'input': "двадцать один год", 'output': "21 год"},
            {'input': "это тест с    несколькими     пробелами между сто двадцать словами", 'output': "это тест с    несколькими     пробелами между 120 словами"},
            {'input': "тысяча двести тридцать четыре", 'output': "1234"},
            {'input': "пять миллионов шестьсот тысяч семьсот восемьдесят девять", 'output': "5600789"},
            {'input': "один миллиард два миллиона три тысячи четыре", 'output': "1002003004"},
            {'input': "двадцать первое сентября", 'output': "21 сентября"},
            {'input': "тысяча девятьсот восемьдесят четвёртый год", 'output': "1984 год"},
            {'input': "пятнадцатое мая", 'output': "15 мая"},
            {'input': "сотый день рождения", 'output': "100 день рождения"},
            {'input': "миллиардный шаг человечества", 'output': "1000000000 шаг человечества"},
            {'input': "третий сезон сериала", 'output': "3 сезон сериала"},
            {'input': "восемьдесят восьмой квартал", 'output': "88 квартал"},
        ]

        if console_output:
            print("Тестирование TextToNumberService:")
            print("=" * 60)

        for idx, case in enumerate(test_cases):
            result = cls.execute(case['input'])
            assert result == case['output'], f"Тест {idx} не пройден: {result} != {case['output']}"
            if console_output:
                print(f"✅ Тест {idx + 1} пройден: '{case['input']}' → '{result}'")

        if console_output:
            print(f"\n🎉 Все {len(test_cases)} тестов пройдены успешно!")
        return True


if __name__ == "__main__":
    TextToNumberService.test(console_output=True)