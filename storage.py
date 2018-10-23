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
            self.privateKeyBytes = keyFile.read()
        try:
            self.privateKey = keys.UmbralPrivateKey.from_bytes(self.privateKeyBytes)
        except Exception as e:
            print(e)
            print('Damaged key file. Delete file and reinit storage')
        else:
            self.publicKey = self.privateKey.get_pubkey()
            self.publicKeyBytes = self.publicKey.to_bytes()

    def init(self, path):
        self.privateKey = keys.UmbralPrivateKey.gen_key()
        privateKeyBytes = self.privateKey.to_bytes()
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            with open(path + '/key.k', 'wb') as keyFile:
                keyFile.write(privateKeyBytes)
        except Exception as e:
            print(e)

    @isInit
    def newKey(self, keyName, keyValue, path):
        keyValue, keyCapsule = pre.encrypt(self.publicKey, keyValue)
        keyCapsule = keyCapsule.to_bytes()
        tx = self._buildTx().newKey(keyName, keyValue, keyCapsule, self.publicKeyBytes)
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
            print('Key is not exist or you not creator')

    @isInit
    def getListOfKeys(self, path):
        keys = self.contract.call().getKeys()
        for key in keys:
            print(key.decode('utf-8'))

    @isInit
    def getKey(self, keyName, path):
        key = self.contract.call().keys(keyName)
        keyExist = key[4]
        if keyExist:
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
                    keyName = keyName.decode('utf-8')
                    with open(path + '/' + keyName + '.s', 'rb') as signatureFile:
                        signature = signatureFile.read()
                    signature = keys.UmbralPublicKey.from_bytes(signature)
                    capsule.set_correctness_keys(
                        delegating = owner,
                        receiving = self.publicKey,
                        verifying = signature
                    )
                    with open(path + '/' + keyName + '.f', 'rb') as cfragFile:
                        cfragsBytes = cfragFile.read()
                    cfrag = fragments.CapsuleFrag.from_bytes(cfragsBytes)
                    capsule.attach_cfrag(cfrag)
                    value = self._decrypt(valueBytes, capsule)
                except Exception as e:
                    print(e)
            finally:
                if value is not None:
                    print(value)
        else:
            print('Key is not exist')

    @isInit
    def share(self, keyName, path, publicKeyFileName):
        key = self.contract.call().keys(keyName)
        keyExist = key[4]
        if keyExist:
            try:
                with open(path + '/' + publicKeyFileName + '.k', 'rb') as publicKeyFile:
                    publicKeyBytes = publicKeyFile.read()
            except Exception as e:
                print(e)
            else:
                try:
                    publicKey = keys.UmbralPublicKey.from_bytes(publicKeyBytes)
                    signingPrivateKey = keys.UmbralPrivateKey.gen_key()
                    signer = signing.Signer(private_key = signingPrivateKey)
                    kfrags = pre.generate_kfrags(
                        delegating_privkey = self.privateKey,
                        signer = signer,
                        receiving_pubkey = publicKey,
                        threshold = 1,
                        N = 1
                    )
                    directory = path + '/' + publicKeyFileName + '/'
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    curveVar = umbral.config.default_curve()
                    paramsVar = params.UmbralParameters(curveVar)
                    capsule = pre.Capsule.from_bytes(key[1], paramsVar)
                    signingPublicKey = signingPrivateKey.get_pubkey()
                    capsule.set_correctness_keys(
                        delegating = self.publicKey,
                        receiving = publicKey,
                        verifying = signingPublicKey
                    )
                    for kfrag in kfrags:
                        cfrag = pre.reencrypt(
                            kfrag = kfrag,
                            capsule = capsule
                        )
                        cfrag = cfrag.to_bytes()
                    keyName = keyName.decode('utf-8')
                    with open(directory + keyName + '.f', 'wb') as cfragFile:
                        cfragFile.write(cfrag)
                    signingPublicKeyBytes = signingPublicKey.to_bytes()
                    with open(directory + keyName + '.s', 'wb') as signatureFile:
                        signatureFile.write(signingPublicKeyBytes)
                except Exception as e:
                    print(e)
                else:
                    print('Done')
        else:
            print('Key is not exist')

    @isInit
    def remove(self, path, keyName):
        tx = self._buildTx().removeKey(keyName)
        result = self._ethTransaction(tx)
        if result:
            print('Key removed')
        else:
            print('Key is not exist or you not creator')

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
