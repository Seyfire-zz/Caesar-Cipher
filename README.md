# Caesar-Cipher

Object oriented approach to representing and implementing a Caesar Cipher form of encryption :)

The Message class is the main parent class. 
It builds a dictionary of ascii upper and lower case letters as keys, and values based on the alphabet shift provided.

The PlaintextMessage class represents a message in plaintext format. 
Methods in this class can use the Ceasar Cipher shift key to return an encrypted version of the message, as well as changing the value of the shift key.

The CiphertextMessage class represents an encrypted message.
Method in this class will attempt to decrypt the message and return a plaintext version.
