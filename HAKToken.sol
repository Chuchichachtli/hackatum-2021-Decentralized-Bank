//SPDX-License-Identifier: Unlicense
pragma solidity 0.7.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v3.2.0-solc-0.7/contracts/token/ERC20/ERC20.sol";

contract HAKToken is ERC20 {

   uint256 public constant STARTING_SUPPLY = 1e24;
   constructor() ERC20("HAKTest", "HAKT") {
      _mint(msg.sender, STARTING_SUPPLY);
   }
}