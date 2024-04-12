import string
from Utils import final_processing


def create_an_incidence_matrix(file_names: list, where_to_write_result: str = 'results/result_matrix.txt'):
    file_names = sorted(set(file_names))  # позбавляємося повторів файлів, якщо вони є
    matrix_of_word_appearance = {}

    counter = 0
    for file in file_names:
        counter += 1
        with open(file, "r", encoding='utf-8') as txt_file:
            file_content = txt_file.readlines()
        for item in file_content:
            array_of_words = item.lower().split()
            for word in array_of_words:
                word = delete_punctuation(word)

                if word not in matrix_of_word_appearance:
                    length = 0
                    for key in matrix_of_word_appearance:
                        length = len(matrix_of_word_appearance[key])
                        break

                    matrix_of_word_appearance[word] = [0] * length
                    matrix_of_word_appearance[word].append(1)
                else:
                    if len(matrix_of_word_appearance[word]) < counter:
                        matrix_of_word_appearance[word].append(1)

        for value in matrix_of_word_appearance.values():
            if len(value) < counter:
                value.append(0)

    result = final_processing(matrix_of_word_appearance, where_to_write_result, 'incidence matrix')
    return result


def create_an_inverted_index(file_names: list, where_to_write_result: str = 'results/result_index.txt'):
    file_names = sorted(set(file_names))  # позбавляємося повторів файлів, якщо вони є
    inverted_index_list = {}

    file_indices = {}
    index = 0
    for file in file_names:
        file_indices[file] = index
        index += 1

    for file in file_names:
        print(file)
        with open(file, "r") as txt_file:
            file_content = txt_file.readlines()
        for item in file_content:
            array_of_words = item.lower().split()
            for word in array_of_words:
                word = delete_punctuation(word)

                inverted_index_list[word] = [] if word not in inverted_index_list else inverted_index_list[word]

                if file_indices[file] not in inverted_index_list[word]:
                    inverted_index_list[word].append(file_indices[file])

    final_processing(inverted_index_list, where_to_write_result, 'inverted index')


def delete_punctuation(word : str):
    while len(word) > 0 and word[0] in string.punctuation:
        word = word[1:]
    while len(word) > 0 and word[-1] in string.punctuation:
        word = word[:-1]

    return word


# create_an_incidence_matrix(file_collection)
# print(create_an_inverted_index(file_collection))


# на моїх даних вийшов такий результат
# incidence matrix size in kb = 575.671
# inverted index size in kb = 331.679
# тобто інвертований індекс займає вдвічі менше місця, ніж матриця інцидентності
# і чим більший розмір колекції, тим більша буде різниця між пам'яттю для зберігання інформації
# про наявність або відсутність терміна в документі
