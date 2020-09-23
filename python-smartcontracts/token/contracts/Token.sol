pragma solidity ^0.6.0;

import "./SafeMath.sol";

contract Token {

    uint256 public total;

    event AddToTotalEvent();

    function addToTotal(uint256 _number) external {
        total += _number;
        emit AddToTotalEvent();
    }
}
