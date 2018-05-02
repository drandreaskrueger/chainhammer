// https://github.com/jpmorganchase/quorum-examples/blob/master/examples/7nodes/simplestorage.sol

pragma solidity ^0.4.15;

contract simplestorage {
  uint public storedData;

  function simplestorage(uint initVal) {
    storedData = initVal;
  }

  function set(uint x) {
    storedData = x;
  }

  function get() constant returns (uint retVal) {
    return storedData;
  }
}



// https://github.com/jpmorganchase/cakeshop/blob/master/cakeshop-api/src/main/resources/contracts/SimpleStorage.sol

/*

pragma solidity ^0.4.9;
contract SimpleStorage {

    uint public storedData;

    event Change(string message, uint newVal);

    function SimpleStorage(uint initVal) {
        Change("initialized", initVal);
        storedData = initVal;
    }

    function set(uint x) {
        Change("set", x);
        storedData = x;
    }

    function get() constant returns (uint retVal) {
        return storedData;
    }

}

*/

// http://web3py.readthedocs.io/en/stable/examples.html#working-with-contracts

/*
contract StoreVar {

    uint8 public _myVar;
    event MyEvent(uint indexed _var);

    function setVar(uint8 _var) public {
        _myVar = _var;
        MyEvent(_var);
    }

    function getVar() public view returns (uint8) {
        return _myVar;
    }

}

*/