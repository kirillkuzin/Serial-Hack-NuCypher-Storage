pragma solidity ^0.4.21;

contract Storage {
    struct Key {
        bytes value;
        bytes capsule;
        bytes owner;
        bytes signature;
    }
    mapping(bytes32 => Key) public keys;
    bytes32[] public listOfKeys;

    function newKey(bytes32 keyName, bytes keyValue, bytes keyCapsule, bytes keyOwner, bytes keySignature) public {
        for (uint i = 0; i < listOfKeys.length; i++) {
            require(keyName != listOfKeys[i]);
        }
        setKey(keyName, keyValue, keyCapsule);
        setKeyOwner(keyName, keyOwner);
        setKeySignature(keyName, keySignature);
        listOfKeys.push(keyName);
    }

    function updateKey(bytes32 keyName, bytes keyValue, bytes keyCapsule) public returns(bool) {
        bool keyIsSet = false;
        for (uint i = 0; i < listOfKeys.length; i++) {
            if (keyName == listOfKeys[i]) {
                keyIsSet = true;
                break;
            }
        }
        require(keyIsSet);
        setKey(keyName, keyValue, keyCapsule);
        return true;
    }

    function getKeys() public constant returns(bytes32[]) {
        return listOfKeys;
    }

    function setKey(bytes32 keyName, bytes keyValue, bytes keyCapsule) private {
        Key storage key = keys[keyName];
        key.value = keyValue;
        key.capsule = keyCapsule;
    }

    function setKeyOwner(bytes32 keyName, bytes keyOwner) private {
        Key storage key = keys[keyName];
        key.owner = keyOwner;
    }

    function setKeySignature(bytes32 keyName, bytes keySignature) private {
        Key storage key = keys[keyName];
        key.signature = keySignature;
    }
}
