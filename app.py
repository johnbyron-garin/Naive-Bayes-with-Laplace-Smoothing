# John Byron C. Garin
# X1L
# 2021-02658

import re
import os # to be able to read files in a folder
import math
from decimal import *

import os

# save each line from the file to an array
def read_files_from_folder(data_num, ham_or_spam):
    folder_path = f"data/data0{data_num}/{ham_or_spam}"
    all_tokens = []  # Will hold all tokens from all files in the folder
    file_count = 0  # To count the number of files read

    # List all files in the folder
    file_list = os.listdir(folder_path)

    for filename in file_list:
        file_path = os.path.join(folder_path, filename)
        try:
            with open(file_path, "r", encoding="Latin-1") as file:
                for line in file:
                    words = line.strip().split()  # Split each line into words using whitespaces
                    all_tokens.extend(words)
                file_count += 1
        except FileNotFoundError:
            print(f"File '{filename}' not found!")

    return all_tokens, file_count

def read_files_from_classify(data_num):
    folder_path = f"data/data0{data_num}/classify"
    all_words = []

    # List all files in the folder
    file_list = os.listdir(folder_path)

    for filename in file_list:
        file_path = os.path.join(folder_path, filename)
        words_from_file = []

        try:
            with open(file_path, "r", encoding="Latin-1") as file:
                for line in file:
                    words = line.strip().split()  # Split each line into words using whitespaces
                    words_from_file.extend(words)
        except FileNotFoundError:
            print(f"File '{filename}' not found!")

        all_words.append(words_from_file)

    return all_words

# removes all non alnum characters from each word
def cleaning_words(words):
    clean_words = []
    for w in words:
        s = re.sub(r'[^a-zA-Z0-9]', '', w)
        if s != '':
            clean_words.append(s.lower())
    return clean_words

# counts the frequency of each word and then creating an array out of it
# saves it to a dictionary that uses the word as keys and the frequency for its value
def add_to_dictionary(clean_words):
    bag_of_words = {}
    for word in clean_words:
        word_lower = word.lower()  # Convert the word to lowercase to ensure case-insensitive counting
        if word_lower in bag_of_words:
            bag_of_words[word_lower] += 1
        else:
            bag_of_words[word_lower] = 1
    
    return bag_of_words

# counts the total words by adding all keys
def total_words(bag_of_words):
    total_words = 0
    for keys in bag_of_words:
        total_words = total_words + bag_of_words[keys]
    return total_words

def clean_BoW(file_lines):
    clean_words = cleaning_words(file_lines)
    return clean_words

def classify_BoW(file_lines):
    clean_words = cleaning_words(file_lines)
    bag_of_words = add_to_dictionary(clean_words)
    return bag_of_words

# returns a list of the unique words when the BoW of ham and spam are unioned
def unique_ham_spam(ham_BoW, spam_BoW):
    keys1 = set(ham_BoW.keys())
    keys2 = set(spam_BoW.keys())
    unique_keys = keys1.union(keys2)
    return len(list(unique_keys))

# counts the number of words new to both ham and spam BoW
def new_word_count(c_BoW, spam_BoW, ham_BoW):
    newWords_count = 0
    for word in c_BoW:
        if (word not in spam_BoW) and (word not in ham_BoW):
            newWords_count = newWords_count + 1
    return newWords_count

# returns the BoW, dictionary size, and total number of words of file lines read from a folder
def exer1(file_lines):
    clean_words = cleaning_words(file_lines)
    bag_of_words = add_to_dictionary(clean_words)
    dictionary_size = len(bag_of_words)
    total_number_words = total_words(bag_of_words) 
    return bag_of_words, dictionary_size, total_number_words

def exer2():
    k = int(input("k value: "))
    num_of_data = 3
    for data in range(1,num_of_data+1):
        ham_file_lines, count_ham = read_files_from_folder(data, "ham")
        spam_file_lines, count_spam = read_files_from_folder(data, "spam")
        ham_BoW, ham_dictionary_size, ham_total_number_words = exer1(ham_file_lines)
        spam_BoW, spam_dictionary_size, spam_total_number_words = exer1(spam_file_lines)
        p_spam = count_spam + k / ((count_spam + count_ham) + (2 * k))
        p_ham = count_ham + k / ((count_spam + count_ham) + (2 * k))
        dSize = unique_ham_spam(ham_BoW, spam_BoW)
        # Compute for P(message|Spam)
        classify_array = read_files_from_classify(data)
        classify_counter = 1
        output_file_name = f"0{data}-classify.out"
        with open(output_file_name, 'w') as f:
            for classify in classify_array:
                c_BoW = clean_BoW(classify)
                p_message_spam = 1
                p_message_ham = 1
                newWords_count = new_word_count(c_BoW, spam_BoW, ham_BoW)
                for word in c_BoW:
                    # Spam =============================
                    if word not in spam_BoW:
                        count_word_spam = 0
                    else:
                        count_word_spam = spam_BoW[word]
                    p_word_spam = Decimal((count_word_spam + k) / (spam_total_number_words + (k * (dSize + newWords_count))))
                    p_message_spam *= p_word_spam

                    # Ham =============================
                    if word not in ham_BoW:
                        count_word_ham = 0
                    else:
                        count_word_ham = ham_BoW[word]
                    p_word_ham = Decimal((count_word_ham + k) / (ham_total_number_words + (k * (dSize + newWords_count))))
                    p_message_ham *= p_word_ham

                p_message_spam = p_message_spam * Decimal(p_spam)
                p_message_ham = p_message_ham * Decimal(p_ham)
                p_spam_message = (p_message_spam) / (p_message_spam + p_message_ham)
                if p_spam_message > 0.5:
                    spam_or_ham = "SPAM"
                else:
                    spam_or_ham = "HAM"
                formatted_counter = str(classify_counter).zfill(3)
                output_line = f"{formatted_counter} {spam_or_ham} {p_spam_message}"
                f.write(output_line + '\n')

                classify_counter = classify_counter + 1

        with open(output_file_name, 'a') as f:
            f.write("\n")
            f.write("HAM\n")
            f.write("Dictionary Size: {}\n".format(ham_dictionary_size))
            f.write("Total Number of Words: {}\n".format(ham_total_number_words))
            f.write("\n")
            f.write("SPAM\n")
            f.write("Dictionary Size: {}\n".format(spam_dictionary_size))
            f.write("Total Number of Words: {}\n".format(spam_total_number_words))

exer2()

