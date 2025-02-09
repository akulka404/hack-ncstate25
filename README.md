# ⚡ **GridWise.AI: Blockchain + AI for Smarter Energy Trading**  

## 🚀 **Overview**  
GridWise.AI is an **AI-powered, blockchain-based energy trading platform** that enables **peer-to-peer (P2P) transactions** between households with **solar energy surplus** and those in need of energy.  
By integrating **deep learning techniques for demand forecasting** and **smart contracts for secure transactions**, GridWise.AI ensures **efficient, transparent, and decentralized** energy distribution.  

## 🔥 **Inspiration**  
Traditional power grids face increasing challenges due to:  
⚡ **Energy waste** from surplus renewable power.  
⚡ **Inefficient load balancing**, leading to grid failures.  
⚡ **Lack of transparency in energy pricing and distribution.**  
⚡ **We're already looking at a considerable depletion of natural resources and must naturally look to renewable forms of energy and its management.**

We wanted to solve this by creating a **decentralized, AI-driven marketplace** where households can:  
✅ **Predict and optimize energy demand.**  
✅ **Trade excess energy using blockchain for trust and transparency.**  
✅ **Ensure fair pricing while reducing dependency on central grids.**  

## ⚡ **What It Does**  
GridWise.AI provides a **fully automated energy trading system** that:  
✅ Uses **AI-powered forecasting** to predict energy demand & supply.  
✅ **Dynamically balances the grid** to optimize power usage.  
✅ Enables **P2P energy trading with blockchain smart contracts** for security.  
✅ **Minimizes energy waste** and **prevents blackouts** through real-time load adjustments.  
✅ **Keeps a solid track of everything happening in the ecosystem.**

## 🔧 **How We Built It**  
1️⃣ **Simulated Solar Energy Data**: Randomized energy generation and consumption for each house. 

2️⃣ **Developed a Blockchain-Based Smart Contract**:  
   - Houses could **buy and sell** energy with **automated transaction execution**.  
   - Prices were dynamically adjusted based on **real-time supply and demand**.  
   - The energy distribution looked both at maximizing seller profit and minimizing buyer loss.
   - In simple terms, we built a stock market for energy.

3️⃣ **Integrated AI-Powered Energy Prediction**:  
   - Used **LSTMs a type of Recurrent Neural Network** to forecast future energy demand.  

4️⃣ **Implemented Load Balancing Algorithm**:  
   - Ensured optimal energy allocation to minimize waste.   

5️⃣ **Built a Web-Based Dashboard**:  
   - Users could **monitor energy transactions** in real-time.  

## 🛠 **Tech Stack & Architecture**  
### **🔗 Blockchain (Decentralized Trading)**  
- **Ethereum Smart Contracts (Solidity)**
- **Hardhat (Local Blockchain Testing)**
- **Web3.py (Blockchain Interaction)**  

### **🧠 AI & Machine Learning (Energy Forecasting & Optimization)**  
- **Time-Series Forecasting** (LSTMs)  
- **A recursive approach and a blockchain based approach for Load Balancing**   

### **📡 IoT & Edge Computing (Data Collection)**  
- **Simulated Smart Meters & Solar Panels**  
- **MongoDB-based real-time data streaming**  
- **Edge Computing with Raspberry Pi and Solar sensors (future integration)**  

### **🌐 Web & API (User Interaction & Trading System)**  
- **Backend:** Mongo Atlas + SQLite3 (Python)  + node.js
- **Frontend:** Streamlit Framework (Python)
- **Database:** MongoDB Atlas (Time-Series Data Storage)  

## 🚧 **Challenges We Ran Into**  
- **Optimizing real-time transactions on the blockchain** to minimize gas fees.  
- **Designing a fair energy pricing model** based on a complex bidding algorithm for both buyers and sellers.  
- **Handling real-time energy fluctuations** while maintaining a stable grid.  

## 🎯 **Accomplishments That We're Proud Of**  
✅ Successfully **integrated AI and blockchain** in a single system.  
✅ Created a **fully automated energy trading smart contract**.  
✅ Developed an **interactive visualization dashboard** for real-time energy monitoring.  
✅ Implemented **real-time P2P energy transactions and smart contracts for verification** on Ethereum & Hardhat.

## 📚 **What We Learned**  
📌 How to **optimize AI-powered energy forecasting** for real-world applications.  
📌 The **challenges of blockchain-based trading**, including security and transaction fees.
📌 The importance of **real-time energy data integration** for smart grid management.  

## 🚀 **Future Roadmap**  
🔹 **Deploy on a Public Blockchain**
🔹 **Integrate Real IoT Smart Meters** for live energy tracking and expose it more sources of renewable energy.  
🔹 **Develop Mobile App for P2P Energy Trading**.  
🔹 **Incorporate Tokenized Carbon Credits** to incentivize green energy.  
🔹 **Work with communities** to build grids that utilize this technology.

## 🛠 **Setup & Deployment**  
### **📌 Prerequisites**  
- **Python 3.x**  
- **Node.js & Hardhat**  
- **MetaMask Wallet**  
- **MongoDB Atlas (for time-series data storage)**  

## How to win? Judging criteria is as follows

- [x] Effectiveness <br>
How effective is the idea or analysis?

- [x] Presentation <br>
How clean and well thought is the presentation?

- [x] Creativity <br>
How unique and out of the box is this idea?

- [x] Usefulness <br>
How useful is this project to the problem?

- [x] Theme <br>
How well does the project fit the track and theme?

## How do you run the blockchain and the load balancing algorithm?

### install requirements 
`pip3 install -r requirements.txt`

---

### run blockchain 

`terminal 1: cd gridwise-blockchain; npm install; npx hardhat compile`

`terminal 1: npx hardhat node`

`terminal 2: cd gridwise-blockchain; npx hardhat run scripts/deploy.js --network localhost`

`terminal 3: python3 energy_shown.py`

---
