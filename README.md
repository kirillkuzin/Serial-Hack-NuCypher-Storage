# Secret Storage

Хранилище секретов, реализованное с помощью Ethereum и NuCypher.

## Commands

help - вывести список доступных комманд и справку по ним:
```
help
```

### init <path> - инициализировать хранилище
Создаст хранилище в текущей директории:
```
init .
```
Создаст хранилище в папке client в текущей директории:
```
init client
```

### new <path> <key_name> <key_value> - добавить новый ключ
Создаст в хранилище из папки storage пару ключ-значение foo-bar:
```
new storage foo bar
```

### update <path> <key_name> <key_value> - обновить существующий ключ
Присвоит в хранилище из текущей директории ключу foo значение bar:
```
update . foo bar1
```

### keys <path> - вывести список ключей
Выведет список ключей из хранилища в текущей директории:
```
keys .
```

### get <path> <key_name> - вывести значение ключа
Выведет значение ключа foo из хранилища в текущей директории. Использует ключ хранилища, если он не подходит, использует ключ из фалйа foo.f, который добывается из share:
```
get . foo
```

### share <path> <key_name> <receiver_name> - открыть доступ к ключу
Откроет доступ к ключу foo из хранилища в текущей директории для developer, если в текущей директории существует файл developer.k, который добывается из pk. Создаст директорию developer, если ее не существует. Создаст файл доступа foo.f в директории developer, который нужно передать developer:
```
share . foo developer
```

### pk <path> <name> - экспортировать свой ключ хранилища для открытия доступа
Создаст файл developer.k, который нужно передать хозяину нужного ключа для открытия доступа:
```
pk . developer
```

## Built With

* [Ethereum](https://www.ethereum.org/) - Blockchain app platform
* [NuCypher](https://www.nucypher.com/) - The privacy layer of the decentralized web
