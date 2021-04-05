import random
import timeit
import pandas as pd

random.seed(0)


def base_convert(num_list, b):
    """ Convert each number in base 10 in num_list into their representation
    in base b in a form of list and find the maximum digit

    :complexity: O(n* logb M); n = the length of num_list; M = the largest number in num_list
    :param num_list: a list of positive integers
    :param b: a number to represent the base
    :return: a list of tuples of the original number and the list
    representing the number in the base b, and the maximum digit
    """
    num_list_base = []
    M = 0
    for num in num_list:
        num_in_base = list_base(num, b)
        if len(num_in_base) > M:
            M = len(num_in_base)
        num_list_base.append((num, num_in_base))
    return num_list_base, M


def list_base(num, b):
    """ Create a list as a representation of num in base b

    :complexity: O(logb num)
    :param num: a number to be converted according to base b
    :param b: a number to represent the base
    :return: a list of numbers which represent the num in base b
    """
    num_base = []
    while num >= 1:
        r = num % b
        num_base.append(r)
        num = num // b
    num_base.reverse()
    return num_base


def numerical_radix_sort(num_list, b):
    """ Sort the numbers in num_list using radix sort according to the base b

    :complexity: O((n + b) ∗ logb M)); n = the length of num_list, M = the largest number in num_list
    :param num_list: a list of positive integers
    :param b: the base
    :return: the sorted list of num_list
    """
    num_list, max_digit = base_convert(num_list, b)  # convert the num according to their bases
    digits = [[] for _ in range(b + 1)]
    index = -1

    # Sort the number from left to right using index
    while abs(index) <= max_digit:
        for i in range(len(num_list)):
            num = num_list[i]
            if abs(index) <= len(num[1]):
                digits[num[1][index]].append(i)
            else:
                digits[0].append(i)
        index -= 1
        temp_list = []
        for i in range(len(digits)):
            for x in digits[i]:
                temp_list.append(num_list[x])
            digits[i] = []
        num_list = temp_list

    # Get the original form of the number in the first element
    for i in range(len(num_list)):
        num_list[i] = num_list[i][0]
    return num_list


def test_bases(num_list):
    """ Count the time in seconds that it takes for num_list to be sorted using
    numerical_radix_sort according to different bases.
    The bases are the powers of 2, starting with an exponent of 1 to 18

    :param num_list: a list of positive integers
    :return: a list of tuples; The first element is the base (integer).
    The second element is the time (seconds) which it took to sort the input list using that base.
    """
    data_output = []
    for base in range(1, 20):
        b = 2 ** base
        start = timeit.default_timer()
        numerical_radix_sort(num_list, b)
        end = timeit.default_timer()
        time = end - start
        data_output.append((base, time))
    return data_output


#   Code for creating a table in the excel using pandas ##########################

def table_radix_sort(tuple_list, filename):
    """ Manage the data to have the list and coloums for to create the table in excel

    :param tuple_list: the data in tuple
    :param filename: the name of the excel file for the data
    """
    table = {
        "Base": [],
        "Runtime": []
    }
    columns = ["Base", "Runtime"]
    for data in tuple_list:
        table["Base"].append(data[0])
        table["Runtime"].append(data[1])
    table_in_excel(filename + '.xlsx', table, columns)


def table_in_excel(filename: str, data: {}, columns: []) -> None:
    """ Generate an excel file from data and columns

    :param filename: the name of the excel file
    :param data: the data for the table
    :param columns: the title for each columns
    """

    # create a table in excel from the data using pandas
    df = pd.DataFrame(data, columns=columns)
    write = pd.ExcelWriter(filename)
    df.to_excel(write, 'Sheet1')
    write.save()


#####################################################################

def scrabble_helper(word_list, char_set_list):
    """ Find the anagrams of char_set_list in word_list

    :complexity : O(nM + qMlog(n)); n = length of word_list,
        M = the number of characters in the longest word in word_list, q = the length of char_set_list
    :param word_list:
    :param char_set_list:
    :return: a list of list containing the anagrams
    """
    anagrams = [[] for _ in range(len(char_set_list))]
    word_sort = []

    # Sort each character in word alphabetically
    for i in range(len(word_list)):
        word_in_char = [x for x in word_list[i]]
        word_sort.append([word_list[i], "".join(word_counting_sort(word_in_char))])

    # Sort each alphabetically word in the second element alphabetically
    word_sort = word_radix_sort(word_sort, True)

    # Sort each character in word alphabetically
    for i in range(len(char_set_list)):
        char_list = [c for c in char_set_list[i]]
        char_sort = "".join(word_counting_sort(char_list))

        # Find the first and last occurrences
        first = first_occurrence_bs(word_sort, char_sort)
        last = last_occurrence_bs(word_sort, char_sort)

        # Append all word_sort[first: last+1] to anagrams
        if first is not None and last is not None:
            for j in range(first, last + 1):
                anagrams[i].append(word_sort[j][0])
        elif first is None and last is not None:
            anagrams[i].append(word_sort[last][0])

    # Sort the each anagram alphabetically
    for i in range(len(anagrams)):
        anagrams[i] = word_radix_sort(anagrams[i])

    return anagrams


def first_occurrence_bs(lst, word):
    """ Using binary search algorithm, finds the first occurrence of word in lst in second element

    :complexity: O(log n); n = the length of lst
    :param lst: a list of tuples
    :param word: target for search
    :return: index of last occurrence
    """
    start = 0
    end = len(lst) - 1

    while start < end - 1:
        mid = (start + end) // 2
        if lst[mid][1] >= word:
            end = mid
        else:
            start = mid

    if len(lst) != 0 and lst[end][1] == word:
        return end
    else:
        return None


def last_occurrence_bs(lst, word):
    """ Using binary search algorithm, finds the last occurrence of word in lst in second element

    :complexity: O(log n); n = the length of lst
    :param lst: a list of tuples
    :param word: target for search
    :return: index of first occurrence
    """
    start = 0
    end = len(lst)

    while start < end - 1:
        mid = (start + end) // 2
        if lst[mid][1] <= word:
            start = mid
        else:
            end = mid

    if len(lst) != 0 and lst[start][1] == word:
        return start
    else:
        return None


def word_counting_sort(char_list):
    """ Sort the character in the char_list alphabetically

    :complexity: O(n); n = length of char_list
    :param char_list: a list f characters
    :return: a sorted char_list in increasing order
    """
    alphabets = [[] for _ in range(26)]
    for i in range(len(char_list)):
        alphabets[ord(char_list[i]) - 97].append(i)
    sort_str_list = []
    for c in range(len(alphabets)):
        for j in alphabets[c]:
            sort_str_list.append(char_list[j])
        alphabets[c] = []
    return sort_str_list


def word_radix_sort(word_list, is_list=False):
    ''' Sort the word_list using radix sort algorithm based on the isList

    :complexity: O(n*M); n = length of word_list,
        M = the number of characters in the longest word in word_list
    :param is_list: a bool
        False: the element in word_list is a string
        True: the element is a list in size 2 and the sorting is based on the 2nd element
    :param word_list: the list of string or list of string to be sorted
    :return: a sorted word_list in increasing order
    '''

    if not word_list:
        return []

    M = 0
    index = -1
    alphabets = [[] for _ in range(27)]  # counting for characters, 0 is " ", 1-26 is a-z

    # Find the length of the longest string (M)
    if is_list is True:
        for i in range(len(word_list)):
            if len(word_list[i][1]) > M:
                M = len(word_list[i][1])
    else:
        M = len(max(word_list))

    # Add spaces " " to match the length of all strings with the longest string (M)
    for i in range(len(word_list)):
        if is_list is True:
            word = word_list[i][1]
            if len(word) < M:
                word_list[i][1] += " " * (M - len(word))
        else:
            word = word_list[i]
            if len(word) < M:
                word_list[i] += " " * (M - len(word))

    # Sort the word_list from index left to right
    while abs(index) <= M:
        for i in range(len(word_list)):
            if is_list is True:
                word = word_list[i][1]
            else:
                word = word_list[i]
            if ord(word[index]) != 32:  # ord(" ") is equal to 32
                alphabets[ord(word[index]) - 96].append(i)
            else:
                alphabets[0].append(i)
        index -= 1
        temp_list = []
        for c in range(len(alphabets)):
            for j in alphabets[c]:
                temp_list.append(word_list[j])
            alphabets[c] = []
        word_list = temp_list

    # Strip the extra spaces that were added
    for i in range(len(word_list)):
        if is_list is True:
            word_list[i][1] = word_list[i][1].strip()
        else:
            word_list[i] = word_list[i].strip()

    return word_list


if __name__ == '__main__':
    data1 = [random.randint(0, 2 ** 8 - 1) for _ in range(10 ** 4)]
    data2 = [random.randint(0, 2 ** 8 - 1) for _ in range(10 ** 5)]
    data3 = [random.randint(0, 2 ** (2 ** 10) - 1) for _ in range(10)]
    data4 = [random.randint(0, 2 ** (2 ** 10) - 1) for _ in range(20)]

    output = test_bases(data1)
    table_radix_sort(output, "data1")
    output = test_bases(data2)
    table_radix_sort(output, "data2")
    output = test_bases(data3)
    table_radix_sort(output, "data3")
    output = test_bases(data4)
    table_radix_sort(output, "data4")
