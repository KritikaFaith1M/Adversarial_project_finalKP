// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AuditNotary {

    string[] public hashes;

    function storeHash(string memory _hash) public {
        hashes.push(_hash);
    }

    function getAuditCount() public view returns (uint256) {
        return hashes.length;
    }

    function getHash(uint index) public view returns (string memory) {
        return hashes[index];
    }
}