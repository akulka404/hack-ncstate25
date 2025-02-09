const hre = require("hardhat");

async function main() {
  const EnergyTrading = await hre.ethers.getContractFactory("EnergyTrading");
  const energyTrading = await EnergyTrading.deploy();

  console.log("✅ EnergyTrading contract deployed to:", energyTrading.target);
}

main()
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
  });
