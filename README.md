# hackatum-2021-Decentralized-Bank

#Quantstamp Hackatum Challenge 2021
# **Phase 1: Building**

The goal of this phase is to develop one smart contract that conforms to a given interface and passes a given test suite. After these contracts are implemented, they must be deployed on the [Goerli test network](https://goerli.net/). Here are the main points and rules:

1. Build a smart contract system that can be used as a [lending platform](https://en.wikipedia.org/wiki/Decentralized_finance).
2. Quantstamp provides the [interface](https://www.notion.so/Functional-Requirements-IBank-Interface-HAK-Token-and-Oracle-Addresses-ce22fe19a5a6461d90dabd89790e7657) that MUST be used for the implementation.
3. Quantstamp provides the address of an [ERC20](https://eips.ethereum.org/EIPS/eip-20) contract called the [HAK token](https://goerli.etherscan.io/address/0xbefeed4cb8c6dd190793b1c97b72b60272f3ea6c), which can be deposited in the bank as collateral for borrowing ETH. You can get Goerli ETH from [https://faucet.paradigm.xyz/](https://faucet.paradigm.xyz/)
4. Quantstamp will provide a [test suite](https://drive.google.com/file/d/15l9Vt_LuuDSiT8g8J0i2QPV6I4xP1fcM/view?usp=sharing) to verify that the implemented code functions properly. Teams that do not pass all tests will be penalized i.e. their final HAK token balance will be divided by the number of tests failed + 1.
5. Teams MUST deploy their smart contract(s) on the Goerli test network by the deadline.
6. The smart contract code MUST be published and verified on Etherscan and publicly available to download on DevPost
7. Teams MUST send Quantstamp the addresses of their contacts via the following [Google Form](https://forms.gle/K41zXcgV38CrA4ku8) by the deadline.
8. The contracts MUST NOT be upgradable.
9. Plagiarism of code is NOT allowed. The code of all teams will be checked with a plagiarism detector. The team that deployed the code first will be considered as the original author of the code. Any team that deploys similar code (according to the plagiarism detection software) later will be considered plagiarism.

## **Phase 2: Breaking**

The goal of this phase is to find and exploit vulnerabilities in the `Bank` contracts of other teams participating in this hackaTUM challenge. Your goal is to gather as many HAK tokens in your Attack Wallet as possible. Here are the main points and rules for this phase: 

1. At the beginning of phase 2, Quantstamp will send each team an equal amount of the HAK token to their Attack Wallet.
2. At the beginning of phase 2, Quantstamp will make an equal deposit of HAK tokens in each team's `Bank` contract and this deposit will not be withdrawn by Quantstamp.
3. Teams may attack the `Bank` smart contracts of other teams to capture HAK tokens and increase their own balance.
4. Teams may try to attack the smart contract token itself to increase their HAK token balance.
5. Teams MUST NOT attempt to perform any physical attacks or social engineering attacks in order to steal HAK tokens.
6. Teams MUST NOT collude and send each other HAK tokens.
7. Before the end of Phase 2, all teams MUST withdraw their deposits from the `Bank` contracts of other teams and send them to their own Attack Wallet. This is aimed to prevent collusion attacks where teams simply deposit all their funds into the same `Bank` contract such that the score of that mean increases.
8. Attacking your own `Bank` to steal the deposits is NOT allowed.

**Failure to comply with ALL these rules will lead to team disqualification.**


### **Functional Requirements**

In the following text, we use the terms "user" and "bank customer" interchangeably. The following functional requirements must be satisfied by the implementation of the smart contract(s):

1. A bank customer's account is represented by their wallet address.
2. A bank customer must be able to deposit an amount higher than 0 of tokens into their own account. Deposits can be made in HAK and ETH for the purpose of this challenge.
3. A bank customer must be able to withdraw only up to the amount they deposited into their own account + interest accrued.
4. When withdrawing a deposit, the user will automatically receive interest on their deposit of 3% per 100 blocks. If a user withdraws their deposit earlier or later than 100 blocks, they will receive a proportional interest amount.
5. A bank customer must be able to deposit multiple times in the same account and if so, the interest should be accounted for each time deposit and withdraw are called by that user.
6. Interest must not be compounding. This means that interest is earned only on the deposited amount and not on the accumulated interest itself.
7. A bank customer must be able to borrow ETH from the bank using the HAK token as collateral.
8. The minimum collateral ratio for any loan is 150%. This means that the value of HAK tokens deposited by the user taking out the loan (plus interest), divided by the ETH value borrowed by the same user (plus interest), must be greater or equal to 150%, that is: `(deposits[account] + accruedInterest[account]) * 10000 / (borrowed[account] + owedInterest[account]) >= 15000`.
9. If the collateral ratio for an outstanding loan goes below 150%, then anyone must be able to repay the loan and receive the collateral tokens in exchange for repaying the loan. We call this a "liquidation" of the loan. During liquidation, the debt of the borrower must be erased AND the borrower loses their deposit, which is transferred to the liquidator.
10. A borrower must be able to repay their loan in full or partially at any point in time if they have not been liquidated.
11. Repaying a loan involves paying the borrowed amount, plus an interest rate of 5% of the borrowed amount, per 100 blocks.
12. Anyone must be able to check the current collateral ratio of any account at any point in time.
13. Each of the 5 state-changing functions defined in the `IBank` interface must emit the corresponding event defined at the top of the interface with the correct parameters as specified in the code comments for each event. The view function in the interface does not need to emit any event.
14. The constructor of the `Bank` contract that you write MUST have exactly 2 input parameters. The first parameter must be the address of the price oracle contract. The second input parameter must be the address of the HAK token contract.

Function-specific requirements are written in the code comments of the mandatory `IBank` interface below.

### **Non-Functional Requirements**

1. The implementation must use Solidity version 0.7.0, that is `pragma solidity 0.7.0` MUST be at the beginning of the source file.

### **The HAK token and its price oracle**

- The HAK token is a typical ERC20 token deployed at this address: [https://goerli.etherscan.io/address/0xbefeed4cb8c6dd190793b1c97b72b60272f3ea6c](https://goerli.etherscan.io/address/0xbefeed4cb8c6dd190793b1c97b72b60272f3ea6c)
- In order to get the price of the HAK token in ETH, which will allow you to compute the collateral ratio, use the following `PriceOracle` contract: [https://goerli.etherscan.io/address/0xc3F639B8a6831ff50aD8113B438E2Ef873845552](https://goerli.etherscan.io/address/0xc3F639B8a6831ff50aD8113B438E2Ef873845552)
- The `PriceOracle` contract implements the following simple interface that should be used when implementing the Bank:

NOTE: The PriceOracle contract has its code published on Etherscan and it may contain vulnerabilities. Attacking the PriceOracle or the HAK token contracts is allowed in Phase 2 of this challenge (see Phase 2 description below).
