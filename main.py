import sys
from storage import Storage

if __name__ == '__main__':
    storage = Storage()
    print('Welcome to secret storage !\nEnter "help" for help')
    while True:
        command = input('->')
        commandArgs = command.split(' ')
        try:
            command = commandArgs[0]
            if command == 'exit':
                break
            elif command == '':
                pass
            elif command == 'help':
                print('\ninit <path> - инициализировать хранилище')
                print('new <path> <key_name> <key_value> - добавить новый ключ')
                print('update <path> <key_name> <key_value> - обновить существующий ключ')
                print('keys <path> - вывести список ключей')
                print('get <path> <key_name> - вывести значение ключа')
                print('share <path> <key_name> <receiver_name> - открыть доступ к ключу')
                print('remove <path> <key_name> - удалить ключ')
                print('pk <path> <name> - экспортировать свой ключ хранилища для открытия доступа\n')
            else:
                path = commandArgs[1]
                if command == 'init':
                    storage.init(path)
                elif command == 'new':
                    keyName = bytes(commandArgs[2], encoding = 'utf-8')
                    keyValue = bytes(commandArgs[3], encoding = 'utf-8')
                    storage.newKey(
                        path = path,
                        keyName = keyName,
                        keyValue = keyValue,
                    )
                elif command == 'update':
                    keyName = bytes(commandArgs[2], encoding = 'utf-8')
                    keyValue = bytes(commandArgs[3], encoding = 'utf-8')
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
                    keyName = bytes(commandArgs[2], encoding = 'utf-8')
                    storage.getKey(
                        path = path,
                        keyName = keyName
                    )
                elif command == 'share':
                    keyName = bytes(commandArgs[2], encoding = 'utf-8')
                    publicKeyFileName = commandArgs[3]
                    storage.share(
                        path = path,
                        keyName = keyName,
                        publicKeyFileName = publicKeyFileName
                    )
                elif command == 'remove':
                    keyName = bytes(commandArgs[2], encoding = 'utf-8')
                    storage.remove(
                        path = path,
                        keyName = keyName
                    )
                elif command == 'pk':
                    name = commandArgs[2]
                    storage.exportKey(
                        path = path,
                        name = name
                    )
        except Exception as e:
            print(e)
            print('Use the help command')
