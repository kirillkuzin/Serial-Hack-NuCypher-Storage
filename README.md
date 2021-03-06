# Secret Storage

Хранилище секретов, реализованное с помощью Ethereum и NuCypher.

## Run

```
python main.py
```

## Commands

### help - вывести список доступных комманд и справку по ним:
```
help
```

### init <path_to_storage> - инициализировать хранилище
Создаст хранилище в текущей директории:
```
init .
```
Создаст хранилище в папке client в текущей директории:
```
init client
```

### new <path_to_storage> <key_name> <key_value> - добавить новый ключ
Создаст в хранилище из папки storage пару ключ-значение foo-bar:
```
new storage foo bar
```

### update <path_to_storage> <key_name> <key_value> - обновить существующий ключ
Присвоит в хранилище из текущей директории ключу foo значение bar:
```
update . foo bar1
```

### keys <path_to_storage> - вывести список ключей
Выведет список ключей из хранилища в текущей директории:
```
keys .
```

### get <path_to_storage> <key_name> - вывести значение ключа
Выведет значение ключа foo из хранилища в текущей директории. Использует ключ хранилища, если он не подходит, использует файлы foo.s и foo.f, который добывается из share:
```
get . foo
```

### share <path_to_storage> <key_name> <receiver_name> - открыть доступ к ключу
Откроет доступ к ключу foo из хранилища в текущей директории для developer, если в текущей директории существует файл developer.k, который добывается из pk. Создаст директорию developer, если ее не существует. Создаст файлы доступа foo.s и foo.f в директории developer, которые нужно передать developer:
```
share . foo developer
```

### remove <path_to_storage> <key_name> - удалить ключ
Удалит ключ foo из хранилища в текущей директории:
```
remove . foo
```

### pk <path_to_storage> <name> - экспортировать свой ключ хранилища для открытия доступа
Создаст файл developer.k, который нужно передать хозяину нужного ключа для открытия доступа:
```
pk . developer
```

## Built With

* [Ethereum](https://www.ethereum.org/) - Blockchain app platform
* [NuCypher](https://www.nucypher.com/) - The privacy layer of the decentralized web
