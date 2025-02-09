// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EnergyTrading {
    struct Trade {
        address seller;
        address buyer;
        uint energyAmount; // kWh (stored as Wei for precision)
        uint pricePerKWh; // ETH per kWh (stored as Wei for precision)
        bool completed;
    }

    mapping(uint => Trade) public trades;
    uint public tradeCount;
    address public admin; // GridWise admin

    constructor() {
        admin = msg.sender;
    }

    function createTrade(address _buyer, uint _energyAmount, uint _pricePerKWh) public {
        trades[tradeCount] = Trade(msg.sender, _buyer, _energyAmount, _pricePerKWh, false);
        tradeCount++;
    }

    function getExactPayment(uint _tradeId) public view returns (uint) {
        Trade storage trade = trades[_tradeId];
        return (trade.energyAmount * trade.pricePerKWh) / 1 ether; // ✅ Fix: Proper scaling
    }

    function completeTrade(uint _tradeId) public payable {
        Trade storage trade = trades[_tradeId];
        require(msg.sender == trade.buyer, "Only buyer can complete trade");
        require(msg.value == getExactPayment(_tradeId), "Incorrect payment"); // ✅ Fix: Use getExactPayment
        require(!trade.completed, "Trade already completed");

        payable(trade.seller).transfer(msg.value); // Send payment to seller
        trade.completed = true;
    }

    function getTrade(uint _tradeId) public view returns (address, address, uint, uint, bool) {
        Trade memory trade = trades[_tradeId];
        return (trade.seller, trade.buyer, trade.energyAmount, trade.pricePerKWh, trade.completed);
    }
}
