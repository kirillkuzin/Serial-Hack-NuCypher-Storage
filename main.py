import sys
from storage import Storage

if __name__ == '__main__':
    storage = Storage()
    try:
        command = sys.argv[1]
        if command == 'help':
            print('init <path> - инициализировать хранилище')
            print('new <path> <key_name> <key_value> - добавить новый ключ')
            print('update <path> <key_name> <key_value> - обновить существующий ключ')
            print('keys <path> - вывести список ключей')
            print('get <path> <key_name> - вывести значение ключа')
            print('share <path> <key_name> <receiver_name> - открыть доступ к ключу')
            print('pk <path> <name> - экспортировать свой ключ хранилища для открытия доступа')
        else:
            path = sys.argv[2]
            if command == 'init':
                storage.init(path)
            elif command == 'new':
                keyName = bytes(sys.argv[3], encoding = 'utf-8')
                keyValue = bytes(sys.argv[4], encoding = 'utf-8')
                storage.newKey(
                    path = path,
                    keyName = keyName,
                    keyValue = keyValue,
                )
            elif command == 'update':
                keyName = bytes(sys.argv[3], encoding = 'utf-8')
                keyValue = bytes(sys.argv[4], encoding = 'utf-8')
                storage.updateKey(
                    path = path,
                    keyName = keyName,
                    keyValue = keyValue,
                )
            elif command == 'keys':
                storage.getListOfKeys(
                    path = path
                )
            elif command == 'get':
                keyName = bytes(sys.argv[3], encoding = 'utf-8')
                storage.getKey(
                    path = path,
                    keyName = keyName
                )
            elif command == 'share':
                keyName = bytes(sys.argv[3], encoding = 'utf-8')
                publicKeyFileName = sys.argv[4]
                storage.share(
                    path = path,
                    keyName = keyName,
                    publicKeyFileName = publicKeyFileName
                )
            elif command == 'pk':
                name = sys.argv[3]
                storage.exportKey(
                    path = path,
                    name = name
                )
    except Exception as e:
        print('Use the help command')
