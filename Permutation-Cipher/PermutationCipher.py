from random import shuffle

class PermutationCipher:
    """
    Permutation Cipher and the associated encryption/decryption functions
    """

    def __init__(self, key=[], keylength=5):
        """Initialize cipher with either a provided key or keylength

        Args:
            key (list, optional): Key as a list of integers, in cycle notation. Defaults to [].
            keylength (int, optional): Length of key to generate. Defaults to 5.
        """

        if key:
            self.KEY = key
        else:
            self.KEY = list(range(keylength))

            # Shuffle this range
            shuffle(self.KEY)
        
    def pad(self, plaintext):
        """Pad plaintext so that all blocks are complete and of the same size

        Args:
            plaintext (str): The plaintext to be

        Returns:
            str: Padded Plaintext
        """

        keylength = len(self.KEY)
        remainder = len(plaintext) % keylength

        if remainder == 0:
            return plaintext

        plaintext += 'x' * (keylength - remainder)
        return plaintext
    
    def process_text(self, text):
        """Process text: Perform padding and split into blocks

        Args:
            text (str): The text string to be processed

        Returns:
            list: List containing the blocks of text
        """
        keylength = len(self.KEY)
        text = self.pad(text)

        # Split text into blocks
        # Example: "ABCDEF" with keylength=2 gets split as [['A', 'B'], ['C', 'D'], ['E', 'F']]
        blocks = [text[i : i + keylength] for i in range(0, len(text), keylength)]

        return blocks

    def permute(self, text_blocks, key):
        """Permute text in each text block as per the key

        Args:
            text_blocks (list): List containing blocks of text
            key (list): The key to use for permutation, in cyclic notation

        Returns:
            str: The permuted text
        """
        keylength = len(key)

        permuted_blocks = []
        for block in text_blocks:
            # Initialize permuted block as original block
            pblock = list(block)

            for i in range(keylength):
                # Character at position KEY[i] goes to KEY[i + 1]
                # Modulus with keylength is taken for indexes
                pblock[key[i % keylength]] = block[key[(i + 1) % keylength]]

            permuted_blocks.append(''.join(pblock))
            permuted_text = ''.join(permuted_blocks)

        return permuted_text
    
    def encrypt(self, plaintext):
        """Encrypt a plaintext with the permutation cipher key

        Args:
            plaintext (str): The plaintext, without any spaces and punctuation

        Returns:
            str: The ciphertext
        """
        plaintext_blocks = self.process_text(plaintext)
        ciphertext = self.permute(plaintext_blocks, self.KEY)
        return ciphertext
    
    def decrypt(self, ciphertext):
        """Decrypt a ciphertext with the permutation cipher key

        Args:
            ciphertext (str): The ciphertext, without any spaces and punctuation

        Returns:
            str: The plaintext, with the trailing padded letters stripped
        """
        # Perform the encryption steps with reversed key
        # and strip off trailing 'x' letters
        ciphertext_blocks = self.process_text(ciphertext)
        plaintext = self.permute(ciphertext_blocks, self.KEY[::-1]).rstrip('x')
        return plaintext

    def get_key(self):
        """Get the cipher Key

        Returns:
            list: List containing integer entries as the key
        """
        return self.KEY
