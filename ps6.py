import string


def load_words(file_name):
    """
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.
    """
    print('Loading word list from file...')
    in_file = open(file_name, 'r')
    line = in_file.readline()
    word_list = line.split()
    print('  ', len(word_list), 'words loaded.')
    in_file.close()
    return word_list


def is_word(word_list, word):
    """
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


def get_story_string():
    """
    Returns: a joke in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story


WORDLIST_FILENAME = 'words.txt'


class Message(object):
    def __init__(self, text):
        """
        text (string): the message's text
        """
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        """
        Used to safely access self.message_text outside of the class

        Returns: self.message_text
        """
        return self.message_text

    def get_valid_words(self):
        """
        Used to safely access a copy of self.valid_words outside of the class

        Returns: a COPY of self.valid_words
        """
        return self.valid_words[:]

    def build_shift_dict(self, shift):
        """
        Creates a dictionary that can be used to apply a cipher to a letter.

        shift (integer): the amount by which to shift every letter of the
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to
                 another letter (string).
        """
        lower_dict = {}
        upper_dict = {}
        lower = string.ascii_lowercase * 2
        upper = string.ascii_uppercase * 2
        count = shift
        for i in range(26):
            lower_dict[lower[i]] = lower[count]
            upper_dict[upper[i]] = upper[count]
            count += 1
        lower_dict.update(upper_dict)
        return lower_dict

    def apply_shift(self, shift):
        """
        Applies the Caesar Cipher to self.message_text with the input shift.

        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        """
        text = ""
        shift_dict = self.build_shift_dict(shift)
        for char in self.get_message_text():
            if char not in string.ascii_letters:
                text = text + char
            else:
                text = text + shift_dict[char]
        return text


class PlaintextMessage(Message):
    def __init__(self, text, shift):
        """
        text (string): the message's text
        shift (integer): the shift associated with this message
        """
        Message.__init__(self, text)
        self.shift = shift
        self.encrypting_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        return str(self.shift)

    def get_encrypting_dict(self):
        """  Returns: a COPY of self.encrypting_dict  """
        return self.encrypting_dict.copy()

    def get_message_text_encrypted(self):
        return self.message_text_encrypted

    def change_shift(self, shift):
        """
        Changes self.shift of the PlaintextMessage and updates other
        attributes determined by shift

        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26
        """
        self.shift = shift
        self.encrypting_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        """
        Initializes a CiphertextMessage object

        text (string): the message's text
        """
        Message.__init__(self, text)
        self.valid_words = load_words(WORDLIST_FILENAME)

    def decrypt_message(self):
        """
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one.

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        """
        best_shift = [0, '', 0]  # [shift, message, valid words]

        for i in range(1, 27):
            valid_words = 0
            for word in self.apply_shift(i).split(' '):
                if is_word(self.valid_words, word):
                    valid_words += 1
            if valid_words > best_shift[2]:
                best_shift = [i, self.apply_shift(i), valid_words]

        return best_shift[0], best_shift[1]


# Example test case (PlaintextMessage)
plaintext = PlaintextMessage('hello', 2)
print('Expected Output: jgnnq')
print('Actual Output:', plaintext.get_message_text_encrypted())

# Example test case (CiphertextMessage)
ciphertext = CiphertextMessage('jgnnq')
print('Expected Output:', (24, 'hello'))
print('Actual Output:', ciphertext.decrypt_message())
