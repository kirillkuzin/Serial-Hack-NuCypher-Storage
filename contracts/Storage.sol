pragma solidity ^0.4.21;

contract Storage {
    struct Key {
        bytes value;
        bytes capsule;
        bytes owner;
        address ownerAddress;
        bool created;
    }
    mapping(bytes32 => Key) public keys;
    bytes32[] public listOfKeys;
    address public owner;

    modifier onlyOwner(bytes32 keyName) {
        Key storage key = keys[keyName];
        require(msg.sender == key.ownerAddress || msg.sender == owner);
        _;
    }

    modifier keyIsCreated(bytes32 keyName) {
        Key storage key = keys[keyName];
        require(key.created);
        _;
    }

    modifier keyNotCreated(bytes32 keyName) {
        Key storage key = keys[keyName];
        require(!key.created);
        _;
    }

    constructor() public {
        owner = msg.sender;
    }

    function newKey(bytes32 keyName, bytes keyValue, bytes keyCapsule, bytes keyOwner) public keyNotCreated(keyName) {
        setKey(keyName, keyValue, keyCapsule);
        setKeyOwner(keyName, keyOwner);
        setKeyOwnerAddress(keyName, msg.sender);
        setKeyState(keyName, true);
        listOfKeys.push(keyName);
    }

    function updateKey(bytes32 keyName, bytes keyValue, bytes keyCapsule) public keyIsCreated(keyName) onlyOwner(keyName) {
        setKey(keyName, keyValue, keyCapsule);
    }

    function removeKey(bytes32 keyName) public keyIsCreated(keyName) onlyOwner(keyName) {
        bytes memory nullValue;
        bytes memory nullCapsule;
        bytes memory nullOwner;
        address nullOwnerAddress;
        setKey(keyName, nullValue, nullCapsule);
        setKeyOwner(keyName, nullOwner);
        setKeyOwnerAddress(keyName, nullOwnerAddress);
        setKeyState(keyName, false);
        for (uint i = 0; i < listOfKeys.length - 1; i++) {
            listOfKeys[i] = listOfKeys[i + 1];
        }
        listOfKeys.length--;
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

    function setKeyOwnerAddress(bytes32 keyName, address keyOwnerAddress) private {
        Key storage key = keys[keyName];
        key.ownerAddress = keyOwnerAddress;
    }

    function setKeyState(bytes32 keyName, bool keyState) private {
        Key storage key = keys[keyName];
        key.created = keyState;
    }
}
