// simplestorage contract
// chainhammer v46

pragma solidity ^0.4.21;

contract simplestorage {
  uint public storedData;

  function set(uint x) {
    storedData = x;        // uses ~26691 gas
    
    // try failing transactions:
    // assert ( 1 == 0 );  // uses up all 90000 given gas
    // revert();           // uses 41686 gas
    // throw;              // same as revert(); 
    // require ( 1 == 0 ); // uses 41714 gas
  }

  function get() constant returns (uint retVal) {
    return storedData;
  }
}

