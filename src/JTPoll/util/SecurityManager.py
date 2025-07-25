import base64, hashlib, secrets, aes, aes_cipher
from aes.utils import *
from aes_cipher import Pbkdf2Sha512

def generateKey(password,installFile):
    sha3_512 = hashlib.sha3_512()
    sha3_256 = hashlib.sha3_256()
    shake_256 = hashlib.shake_256()
    pdb = Pbkdf2Sha512(1024 * 1024)
    password = base64.b64encode(password.encode())
    sha3_512.update(password)
    salt = sha3_512.digest()
    preKey = pdb.DeriveKey(password, salt)
    sha3_256.update(preKey)
    shake_256.update(preKey)
    mainKey = sha3_256.digest()
    mainIV = shake_256.digest(16)
    crypt = aes.aes(int2arr8bit(bytes2int(mainKey),32), 256,"CBC", "PKCS#7", int2arr8bit(bytes2int(mainIV),16))
    mainKey,mainIV,shake_256, sha3_512, sha3_256, pdb, password = None,None,None,None,None,None,None
    secureKey = secrets.token_bytes(32)
    secureIV = secrets.token_bytes(16)
    secureKey = crypt.enc(int2arr8bit(bytes2int(secureKey),32))
    secureIV = crypt.enc(int2arr8bit(bytes2int(secureIV),16))
    verificationCheck = crypt.enc(int2arr8bit(bytes2int("JTPoll".encode()),6))
    secureKey = base64.b64encode(int2bytes(arr8bit2int(secureKey))).decode()
    secureIV = base64.b64encode(int2bytes(arr8bit2int(secureIV))).decode()
    verificationCheck = base64.b64encode(int2bytes(arr8bit2int(verificationCheck))).decode()
    writer = installFile.open("w+")
    writer.write(secureKey + '\n' + secureIV + '\n' + verificationCheck)
    writer.flush()
    writer.close()
def GetCrypt(password,installFile):
    sha3_512 = hashlib.sha3_512()
    sha3_256 = hashlib.sha3_256()
    shake_256 = hashlib.shake_256()
    pdb = Pbkdf2Sha512(1024 * 1024)
    password = base64.b64encode(password.encode())
    sha3_512.update(password)
    salt = sha3_512.digest()
    preKey = pdb.DeriveKey(password, salt)
    sha3_256.update(preKey)
    shake_256.update(preKey)
    mainKey = sha3_256.digest()
    mainIV = shake_256.digest(16)
    crypt = aes.aes(int2arr8bit(bytes2int(mainKey),32), 256,"CBC", "PKCS#7", int2arr8bit(bytes2int(mainIV),16))
    mainKey,mainIV,shake_256, sha3_512, sha3_256, pdb, password = None,None,None,None,None,None,None
    secureKey = installFile.open("r").readlines()[0]
    secureIV = installFile.open("r").readlines()[1]
    secureKey = base64.b64decode(secureKey)
    secureIV = base64.b64decode(secureIV)
    keySize = len(secureKey)
    ivSize = len(secureIV)
    secureKey = crypt.dec(int2arr8bit(bytes2int(secureKey),keySize))
    secureIV = crypt.dec(int2arr8bit(bytes2int(secureIV),ivSize))
    retcrypt = aes.aes(secureKey,256,"CBC","PKCS#7", secureIV)
    secureKey = None
    secureIV = None
    crypt = None
    return retcrypt

def CheckPassword(password,installFile):
    sha3_512 = hashlib.sha3_512()
    sha3_256 = hashlib.sha3_256()
    shake_256 = hashlib.shake_256()
    pdb = Pbkdf2Sha512(1024 * 1024)
    sha3_512.update(base64.b64encode(password.encode()))
    salt = sha3_512.digest()
    preKey = pdb.DeriveKey(base64.b64encode(password.encode()), salt)
    sha3_256.update(preKey)
    shake_256.update(preKey)
    mainKey = sha3_256.digest()
    mainIV = shake_256.digest(16)
    crypt = aes.aes(int2arr8bit(bytes2int(mainKey), 32), 256, "CBC", "PKCS#7", int2arr8bit(bytes2int(mainIV), 16))
    mainKey, mainIV, shake_256, sha3_512, sha3_256, pdb, password = None, None, None, None, None, None, None
    verificationCheck = installFile.open("r").readlines()[2]
    verificationCheckLen = len(base64.b64decode(verificationCheck.encode()))
    verificationCheck = crypt.dec(int2arr8bit(bytes2int(base64.b64decode(verificationCheck.encode())),verificationCheckLen))
    verificationCheck = int2bytes(arr8bit2int(verificationCheck)).decode()
    return verificationCheck == "JTPoll"

def SaveToken(widget,password,installFile,token,installFolder):
    if(CheckPassword(password,installFile)):
        crypt = GetCrypt(password,installFile)
        password = None
        token = int2bytes(arr8bit2int(crypt.enc(int2arr8bit(bytes2int(token.encode()),len(token.encode())))))
        token = base64.b64encode(token).decode()
        writer = installFolder.joinpath("JTPollBot.dat").open("w+")
        writer.write(token)
        writer.flush()
        writer.close()
        pass
    else:
        QMessageBox.information(widget, "Authorization Error", "Password Invalid\nApplication Closing")
        sys.exit(5)
