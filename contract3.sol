
// http://web3py.readthedocs.io/en/stable/examples.html#working-with-contracts

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

