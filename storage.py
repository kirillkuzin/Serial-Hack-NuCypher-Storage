import umbral
import os
from umbral import pre, keys, signing, curve, params, fragments
from ethereum_core import Contract

class Storage(Contract):
    def __init__(self):
        super().__init__()
        umbral.config.set_default_curve()
        self.cfrags = list()

    def isInit(func):
        def wrapper(self, **kwargs):
            path = kwargs['path']
            try:
                self.auth(path)
            except Exception as e:
                print(e)
                print('Storage is not init')
            else:
                return func(self, **kwargs)
        return wrapper

    def auth(self, path):
        with open(path + '/key.k', 'rb') as keyFile:
            keysFromFile = keyFile.read().split(b'\r\n')
            self.privateKeyBytes = keysFromFile[0]
            self.signingPrivateKeyBytes = keysFromFile[1]
        try:
            self.privateKey = keys.UmbralPrivateKey.from_bytes(self.privateKeyBytes)
            self.signingPrivateKey = keys.UmbralPrivateKey.from_bytes(self.signingPrivateKeyBytes)
        except Exception as e:
            print(e)
            print('Damaged key file. Delete file and reinit storage')
        else:
            self.publicKey = self.privateKey.get_pubkey()
            self.publicKeyBytes = self.publicKey.to_bytes()
            self.signingPublicKey = self.signingPrivateKey.get_pubkey()
            self.signingPublicKeyBytes = self.signingPublicKey.to_bytes()
            self.signer = signing.Signer(private_key = self.signingPrivateKey)

    def init(self, path):
        self.privateKey = keys.UmbralPrivateKey.gen_key()
        privateKeyBytes = self.privateKey.to_bytes()
        self.signingPrivateKey = keys.UmbralPrivateKey.gen_key()
        signingPrivateKeyBytes = self.signingPrivateKey.to_bytes()
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            with open(path + '/key.k', 'wb') as keyFile:
                keyFile.write(privateKeyBytes)
                keyFile.write(b'\r\n')
                keyFile.write(signingPrivateKeyBytes)
        except Exception as e:
            print(e)
        else:
            print('Init')

    @isInit
    def newKey(self, keyName, keyValue, path):
        keyValue, keyCapsule = pre.encrypt(self.publicKey, keyValue)
        keyCapsule = keyCapsule.to_bytes()
        tx = self._buildTx().newKey(keyName, keyValue, keyCapsule, self.publicKeyBytes, self.signingPublicKeyBytes)
        result = self._ethTransaction(tx)
        if result:
            print('Key added')
        else:
            print('Key is already exist')

    @isInit
    def updateKey(self, keyName, keyValue, path):
        keyValue, keyCapsule = pre.encrypt(self.publicKey, keyValue)
        keyCapsule = keyCapsule.to_bytes()
        tx = self._buildTx().updateKey(keyName, keyValue, keyCapsule)
        result = self._ethTransaction(tx)
        if result:
            print('Key updated')
        else:
            print('Key is not exist')

    @isInit
    def getListOfKeys(self, path):
        keys = self.contract.call().getKeys()
        for key in keys:
            print(key.decode('utf-8'))

    @isInit
    def getKey(self, keyName, path):
        key = self.contract.call().keys(keyName)
        curveVar = umbral.config.default_curve()
        paramsVar = params.UmbralParameters(curveVar)
        capsule = pre.Capsule.from_bytes(key[1], paramsVar)
        valueBytes = key[0]
        value = None
        try:
            value = self._decrypt(valueBytes, capsule)
        except:
            try:
                owner = keys.UmbralPublicKey.from_bytes(key[2])
                signature = keys.UmbralPublicKey.from_bytes(key[3])
                keyName = keyName.decode('utf-8')
                with open(path + '/' + keyName + '.f', 'rb') as shareFile:
                    kfragsBytes = shareFile.read()
                capsule.set_correctness_keys(
                    delegating = owner,
                    receiving = self.publicKey,
                    verifying = signature
                )
                kfrag = fragments.KFrag.from_bytes(kfragsBytes)
                cfrag = pre.reencrypt(
                    kfrag = kfrag,
                    capsule = capsule
                )
                capsule.attach_cfrag(cfrag)
                value = self._decrypt(valueBytes, capsule)
            except Exception as e:
                print(e)
        finally:
            if value is not None:
                print(value)

    @isInit
    def share(self, keyName, path, publicKeyFileName):
        try:
            with open(path + '/' + publicKeyFileName + '.k', 'rb') as publicKeyFile:
                publicKeyBytes = publicKeyFile.read()
        except Exception as e:
            print(e)
        else:
            try:
                publicKey = keys.UmbralPublicKey.from_bytes(publicKeyBytes)
                kfrags = pre.generate_kfrags(
                    delegating_privkey = self.privateKey,
                    signer = self.signer,
                    receiving_pubkey = publicKey,
                    threshold = 1,
                    N = 1
                )
                directory = path + '/' + publicKeyFileName + '/'
                if not os.path.exists(directory):
                    os.makedirs(directory)
                keyName = keyName.decode('utf-8')
                with open(directory + keyName + '.f', 'wb') as shareFile:
                    for kfrag in kfrags:
                        kfragBytes = kfrag.to_bytes()
                        shareFile.write(kfragBytes)
            except Exception as e:
                print(e)
            else:
                print('Done')

    @isInit
    def exportKey(self, path, name):
        try:
            with open(path + '/' + name + '.k', 'wb') as publicKeyFile:
                publicKeyFile.write(self.publicKeyBytes)
        except Exception as e:
            print(e)

    def _decrypt(self, ciphertext, capsule):
        value = pre.decrypt(
            ciphertext = ciphertext,
            capsule = capsule,
            decrypting_key = self.privateKey
        ).decode('utf-8')
        return value
