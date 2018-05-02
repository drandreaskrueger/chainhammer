// https://github.com/jpmorganchase/quorum-examples/blob/master/examples/7nodes/simplestorage.sol

/*

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

*/

// https://github.com/jpmorganchase/cakeshop/blob/master/cakeshop-api/src/main/resources/contracts/SimpleStorage.sol

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