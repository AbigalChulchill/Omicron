from cryptography.fernet import Fernet


class Encryptor:

    def __init__(self):

        self.alpha_mass = 'sfbenf/cvhgjyft/l'

    def encrypt_String(self,input_string):

        gibl = ''.join(chr(ord(letter)-1) for letter in self.alpha_mass)

        #encode string to bytes
        encoded = input_string.encode()

        #get key
        file = open(gibl,'rb')
        key = file.read()
        file.close()

        #encrypt with key
        f = Fernet(key)
        encrypted = f.encrypt(encoded)

        return encrypted

    def decrypt_String(self,encrypted_string):

        gibl = ''.join(chr(ord(letter)-1) for letter in self.alpha_mass)

        #get key
        file = open(gibl,'rb')
        key = file.read()
        file.close()

        f = Fernet(key)
        decrypted = decrypted = f.decrypt(encrypted_string)

        #encode from bytes to text
        original_string = decrypted.decode()

        return original_string


    def decrypt_Bytes_As_String(self,encrypted_string):



        filter_string = str(encrypted_string)[2:-1]
        #print(filter_string)
        as_bytes = filter_string.encode('utf_8')
        #print(as_bytes)
        decrypt_a_string = self.decrypt_String(as_bytes)
        #print(decrypt_a_string)
        return decrypt_a_string






if __name__ == '__main__':

    e = Encryptor()

    encrypt_a_string = e.encrypt_String('defsrrdbpzhtwnlu')
    print(encrypt_a_string)

    my_string = "b'gAAAAABh-LB1q6zyHCQ50yWp-WBbmXyFruCo_ECQzBHIus4kNIu4VWGwNAIzbYmioFyIw4Mm3FMtRyMvaoTyvMWl461sPPAeV12zNVhheAjNG95-jijs9Hg='"
    dec = e.decrypt_Bytes_As_String(my_string)
    print(dec)

    #defsrrdbpzhtwnlu

    #decrypt_a_string = e.decrypt_Bytes_As_String("b'gAAAAABh0XW7hywvHrpTPUzovj7gg=='")
    #print(decrypt_a_string)







