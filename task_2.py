import requests
from collections import defaultdict
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor

def map_function(text):
    words = text.split()
    return [(word.lower(), 1) for word in words]

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(shuffled_values):
    reduced = {}
    for key, values in shuffled_values:
        reduced[key] = sum(values)
    return reduced

def map_reduce(text):
    mapped_values = map_function(text)

    shuffled_values = shuffle_function(mapped_values)

    reduced_values = reduce_function(shuffled_values)

    return reduced_values

def visualize_top_words(word_counts, top_n=10):
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
    words, counts = zip(*sorted_words)

    plt.barh(words, counts, color='skyblue')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.title(f'Top {top_n} Most Frequent Words')
    plt.gca().invert_yaxis()
    plt.show()

def fetch_text_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

if __name__ == '__main__':
    url = input("Введіть URL для аналізу тексту: ")
    
    try:
        with ThreadPoolExecutor() as executor:
            future = executor.submit(fetch_text_from_url, url)
            text = future.result()

        word_counts = map_reduce(text)

        visualize_top_words(word_counts, top_n=10)
    except requests.exceptions.RequestException as e:
        print(f"Помилка завантаження тексту: {e}")
    except Exception as e:
        print(f"Невідома помилка: {e}")