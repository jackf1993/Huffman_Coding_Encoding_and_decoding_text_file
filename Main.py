'''
    Title: Huffman Coding to Encode and Decode text files
    Author: Jack Farah
    Inspiration and Code Credit: Bhrigu Srivastava - https://www.youtube.com/watch?v=JCOph23TQTY&t=1421s
    Description: Creating a custom Huffman Tree to encode and decode a text file using a min priority heap
                 Steps: Compress:
                        1) Build Frequency dictionary
                        2) Build priority queue with min heap
                        3) Build huffman tree by selecting 2 min nodes and merging them
                        4) Assign codes to characters by traversing the tree from root
                        5) Encoding the input text by replacing character with its code
                        6) Add some padding to ensure 8 bit overall length of code
                        7) Store this padded information at the start of the overall encoded bit stream
                        8) Write the result to an output binary file
                        Decompress:
                        1) Read binary file
                        2) Read padding information and remove padded buts
                        3) Decode the bits by reading the bits and replacing the valid Huffman Code buts with
                           the character values
                        4) Save the decoded data into output file

    Overall Time and Space Complexity: Compression - O(nlogn) (time)
                                                     O(n) (space)
                                       Decompression - O(k) (time) where k is the size of compressed data
                                                       O(n) (space)
'''

# Import necessary libraries
import heapq
import os


# create huffman class
class HuffmanCoding:
    # init function, create variables
    def __init__(self, path):
        self.path = path  # file path
        self.heap = []  # heap for huffman code
        self.codes = {}  # dictionary to store character related to their binary code
        self.reverse_mapping = {}  # dictionary for decompression

    # custom heap node class to create nodes for huffman tree
    class HeapNode:
        # init function, create variables
        def __init__(self, char, freq):
            self.char = char  # character variable
            self.freq = freq  # frequency variable
            self.left = None  # left variable for tracking heap
            self.right = None  # right variable for tracking heap

        # less than (lt) function to check for swaps
        def __lt__(self, other):
            return self.freq < other.freq

        # equal (eq) function to check for equal situation
        def __eq__(self, other):
            if other == None:  # do nothing if node is empty
                return False
            if not isinstance(other, HeapNode):  # do nothing if node is not of object HeapNode
                return False
            return self.freq == other.freq

    # creating the frequency dictionary method
    def make_frequency_dict(self, text):
        frequency = {}
        for ch in text:
            if not ch in frequency:
                frequency[ch] = 0
            frequency[ch] += 1
        return frequency

    # creating the min priority heap method
    def make_heap(self, frequency):
        for key in frequency:
            node = self.HeapNode(key, frequency[key])
            heapq.heappush(self.heap, node)

    # merging the codes method to create huffman tree. This is used to ensure min priority heap
    def merge_codes(self):
        while (len(self.heap) > 1):
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = self.HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)

    # helper method for make_codes method. converts the characters to binary
    def make_codes_helper(self, node, current_code):
        if node == None:
            return

        if node.char != None:
            self.codes[node.char] = current_code
            self.reverse_mapping[current_code] = node.char

        self.make_codes_helper(node.left, current_code + '0')
        self.make_codes_helper(node, current_code + '1')

    # make codes method in order to initiate the character conversion into binary codes
    def make_codes(self):
        root = heapq.heappop(self.heap)
        current_code = ''
        self.make_codes_helper(root, current_code)

    # get encoded text method
    def get_encoded_text(self, text):
        encoded_text = ''
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    # padding encoded text method to ensure 8 bit length
    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += '0'

        padded_info = '{0:08b}'.format(extra_padding)
        encoded_text = padded_info + encoded_text

        return encoded_text

    # get byte array for decompression
    def get_byte_array(self, padded_encoded_text):
        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i + 8]
            b.append(int(byte, 2))

        return b

    # compression method to read, compress, and write text file
    def compress(self):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + '.bin'

        with open(self.path, 'r') as file, open(output_path, 'wb') as output:
            text = file.read()
            text = text.rstrip()

            frequency = self.make_frequency_dict(text)

            self.make_heap(frequency)
            self.merge_codes()
            self.make_codes()

            encode_text = self.get_encoded_text(text)
            padding_encoded_text = self.pad_encoded_text(encode_text)

            b = self.get_byte_array(padding_encoded_text)
            output.write(bytes(b))

        print('Compressed')
        return output_path

    # remove padding for decompression
    def remove_padding(self, bit_string):
        padded_info = bit_string[:8]
        extra_padding = int(padded_info, 2)

        bit_string = bit_string[8:]
        encoded_text = bit_string[:-1 * extra_padding]

        return encoded_text

    # process for decoding text
    def decode_text(self, encoded_text):
        current_code = ''
        decoded_text = ''

        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ''

            return decoded_text

    # decompression method to read, decompress, and write text file
    def decompress(self, input_path):
        filename, file_extension = os.path.splitext(input_path)
        output_path = filename + "_decompressed" + ".txt"

        with open(input_path, 'rb') as file, open(output_path, 'r') as output:
            bit_string = ''

            byte = file.read(1)
            while len(byte) > 0:
                byte = ord(byte)
                bits = bin(byte).rjust(8, '0')
                bit_string += bits
                byte = file.read(1)

            encoded_text = self.remove_padding(bit_string)
            decoded_text = self.decode_text(encoded_text)

            output.write(decoded_text)

        print('Decompressed')
        return output_path
