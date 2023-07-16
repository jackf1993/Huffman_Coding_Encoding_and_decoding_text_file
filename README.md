# Huffman_Coding_Encoding_and_decoding_text_file
Creating a custom Huffman Tree to encode and decode a text file using a min priority heap
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
