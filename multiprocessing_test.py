import multiprocessing
import time
from pathlib import Path


# Функція для пошуку ключових слів у файлах
def search_keywords_in_files(files, keywords, queue):
    results = {keyword: [] for keyword in keywords}
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                for keyword in keywords:
                    if keyword in content:
                        results[keyword].append(file)
        except Exception as e:
            print(f"Error reading file {file}: {e}")
    queue.put(results)


def main_multiprocessing(files, keywords):
    # Розподілення файлів між процесами
    num_processes = 4
    files_per_process = len(files) // num_processes
    processes = []
    queue = multiprocessing.Queue()
    start_time = time.time()

    for i in range(num_processes):
        start_index = i * files_per_process
        end_index = None if i == num_processes - 1 else (i + 1) * files_per_process
        process_files = files[start_index:end_index]
        process = multiprocessing.Process(target=search_keywords_in_files, args=(process_files, keywords, queue))
        processes.append(process)
        process.start()

    results = {keyword: [] for keyword in keywords}
    for process in processes:
        process.join()
        process_results = queue.get()
        for keyword, files in process_results.items():
            results[keyword].extend(files)

    end_time = time.time()
    print(f"Multiprocessing version took {end_time - start_time:.2f} seconds")
    return results


if __name__ == "__main__":
    files = list(Path('/Users/viktoriianazaruk/goit-cs-hw-04').rglob('*.txt'))  # Замініть 'path/to/text/files' на відповідний шлях
    keywords = ['keyword1', 'keyword2', 'keyword3']  # Замініть ключові слова на потрібні
    results = main_multiprocessing(files, keywords)
    print(results)
