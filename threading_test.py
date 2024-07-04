import threading
import time
from pathlib import Path


# Функція для пошуку ключових слів у файлах
def search_keywords_in_files(files, keywords, results):
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                for keyword in keywords:
                    if keyword in content:
                        results[keyword].append(file)
        except Exception as e:
            print(f"Error reading file {file}: {e}")


def main_threading(files, keywords):
    # Розподілення файлів між потоками
    num_threads = 4
    files_per_thread = len(files) // num_threads
    threads = []
    results = {keyword: [] for keyword in keywords}
    start_time = time.time()

    for i in range(num_threads):
        start_index = i * files_per_thread
        end_index = None if i == num_threads - 1 else (i + 1) * files_per_thread
        thread_files = files[start_index:end_index]
        thread = threading.Thread(target=search_keywords_in_files, args=(thread_files, keywords, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Threading version took {end_time - start_time:.2f} seconds")
    return results


if __name__ == "__main__":
    files = list(Path('/Users/viktoriianazaruk/goit-cs-hw-04').rglob('*.txt'))

    keywords = ['keyword1', 'keyword2', 'keyword3']  # Замініть ключові слова на потрібні
    results = main_threading(files, keywords)
    print(results)
