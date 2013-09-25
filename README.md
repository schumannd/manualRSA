manualRSA
=========

a python tool to manually encrypt a text file character by character using the RSA encryption system. This is NOT a safe implementation as it can easily be cracked. Please use only for educational purposes.


usage
=====
        create key and encrypt:

        python manualRSA.py [/path/to/clearTextFile]


        decryption:

        python manualRSA.py [/path/to/cypherFile [/path/to/privateKeyD]


        encrypt with existing key:

        python manualRSA.py [/path/to/clearTextFile] [/path/to/publicKeyN] [/path/to/publicKeyE]
