import timeit
import random

def build_shift_table(pattern):
    """Створити таблицю зсувів для алгоритму Боєра-Мура."""
    table = {}
    length = len(pattern)
    # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
    # Створюємо таблицю зсувів для патерну (підрядка)
    shift_table = build_shift_table(pattern)
    i = 0  # Ініціалізуємо початковий індекс для основного тексту

    # Проходимо по основному тексту, порівнюючи з підрядком
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1  # Починаємо з кінця підрядка

        # Порівнюємо символи від кінця підрядка до його початку
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1  # Зсуваємось до початку підрядка

        # Якщо весь підрядок збігається, повертаємо його позицію в тексті
        if j < 0:
            return i  # Підрядок знайдено

        # Зсуваємо індекс i на основі таблиці зсувів
        # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # Якщо підрядок не знайдено, повертаємо -1
    return -1

def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено

def polynomial_hash(s, base=256, modulus=101):
    """
    Повертає поліноміальний хеш рядка s.
    """
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def rabin_karp_search(main_string, substring):
    # Довжини основного рядка та підрядка пошуку
    substring_length = len(substring)
    main_string_length = len(main_string)
    
    # Базове число для хешування та модуль
    base = 256 
    modulus = 101  
    
    # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)
    
    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(base, substring_length - 1) % modulus
    
    # Проходимо крізь основний рядок
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1

# main_string = "Being a developer is not easy"
# substring = "developer"

# position = rabin_karp_search(main_string, substring)
# if position != -1:
#     print(f"Substring found at index {position}")
# else:
#     print("Substring not found")


def main():
    
    text1 =open("1.txt", "r",  encoding='utf-8',
                 errors='ignore').read()
    text2 =open("2.txt", "r",  encoding='utf-8',
                 errors='ignore').read()

    res = timeit.timeit(lambda: boyer_moore_search(text1, "boyer_moore_search"), number=1)
    print(f"Час Боєра-Мура для вигаданого підрядка: в тексті 1 {res} сек")
          
    res = timeit.timeit(lambda: boyer_moore_search(text1, "Recommender"), number=1)
    print(f"Час Боєра-Мура з підрядком, що існує в тексті 1 {res} сек")
    
    res = timeit.timeit(lambda: boyer_moore_search(text2, "boyer_moore_search"), number=1)
    print(f"Час Боєра-Мура для вигаданого підрядка в тексті 2: {res} сек") 
      
    res = timeit.timeit(lambda: boyer_moore_search(text2, "Recommender"), number=1)
    print(f"Час Боєра-Мура з підрядком, що існує в тексті 2 {res} сек")
   
  
    print("\n")
    
    res = timeit.timeit(lambda: kmp_search(text1, "boyer_moore_search"), number=1)
    print(f"Час Кнута-Морріса-Пратта для вигаданого підрядка: в тексті 1 {res} сек")
          
    res = timeit.timeit(lambda: kmp_search(text1, "Recommender"), number=1)
    print(f"Час Кнута-Морріса-Пратта з підрядком, що існує в тексті 1 {res} сек")
    
    res = timeit.timeit(lambda: kmp_search(text2, "boyer_moore_search"), number=1)
    print(f"Час Кнута-Морріса-Пратта для вигаданого підрядка в тексті 2: {res} сек") 
      
    res = timeit.timeit(lambda: kmp_search(text2, "Recommender"), number=1)
    print(f"Час Кнута-Морріса-Пратта з підрядком, що існує в тексті 2 {res} сек")
   
    print("\n")
    
    res = timeit.timeit(lambda: rabin_karp_search(text1, "boyer_moore_search"), number=1)
    print(f"Час Рабіна-Карпа для вигаданого підрядка: в тексті 1 {res} сек")
          
    res = timeit.timeit(lambda: rabin_karp_search(text1, "Recommender"), number=1)
    print(f"Час Рабіна-Карпа з підрядком, що існує в тексті 1 {res} сек")
    
    res = timeit.timeit(lambda: rabin_karp_search(text2, "boyer_moore_search"), number=1)
    print(f"Час Рабіна-Карпа для вигаданого підрядка в тексті 2: {res} сек") 
      
    res = timeit.timeit(lambda: rabin_karp_search(text2, "Recommender"), number=1)
    print(f"Час Рабіна-Карпа з підрядком, що існує в тексті 2 {res} сек")
   
# Час Боєра-Мура для вигаданого підрядка: в тексті 1 0.000344442087225616 сек
# Час Боєра-Мура з підрядком, що існує в тексті 1 0.0005282131023705006 сек
# Час Боєра-Мура для вигаданого підрядка в тексті 2: 0.0004553670296445489 сек
# Час Боєра-Мура з підрядком, що існує в тексті 2 0.0006315680220723152 сек

# Час Кнута-Морріса-Пратта для вигаданого підрядка: в тексті 1 0.00158033799380064 сек
# Час Кнута-Морріса-Пратта з підрядком, що існує в тексті 1 0.001523945014923811 сек
# Час Кнута-Морріса-Пратта для вигаданого підрядка в тексті 2: 0.0022975760512053967 сек
# Час Кнута-Морріса-Пратта з підрядком, що існує в тексті 2 0.0020435439655557275 сек

# Час Рабіна-Карпа для вигаданого підрядка: в тексті 1 0.005175531026907265 сек
# Час Рабіна-Карпа з підрядком, що існує в тексті 1 0.00467367994133383 сек
# Час Рабіна-Карпа для вигаданого підрядка в тексті 2: 0.007041951059363782 сек
# Час Рабіна-Карпа з підрядком, що існує в тексті 2 0.006749309948645532 сек
# За результатами всіх тестів, ми можемо сказати, що серед алгоритмів 

# Боєра-Мура, Кнута-Морріса-Пратта та Рабіна-Карпа пошуку підрядків у тексті, в нас найшвидшим є алгоритм Боєра-Мура.
# Другий за швидкістю в нас алгоритм Кнута-Морріса-Пратта. 
# І найповільніший з цих трьох у нас алгоритм Рабіна-Карпа


if __name__ == "__main__":
    main()
