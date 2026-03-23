# Adversarial Attack ML Model with Blockchain Audit
This project implements a secure framework for auditing Machine Learning model robustness. It simulates adversarial attacks on a ResNet18 architecture and records the attack artifacts and results onto a Blockchain to ensure a tamper-proof, decentralized audit trail.

## Project Overview
**Model**: ResNet18 trained on CIFAR-10.

**Attacks Simulated***: Fast Gradient Sign Method (FGSM) and Projected Gradient Descent (PGD).

***Audit Mechanism***: Attack metadata and results are stored via Solidity Smart Contracts.

***Storage***: Attack artifacts (images/logs) are offloaded to IPFS, with hashes stored on-chain.

***Goal***: To provide accountability and transparency in the ML inference phase.


# Project Structure

--------------------------------

<img width="191" height="588" alt="Screenshot 2026-03-23 182744" src="https://github.com/user-attachments/assets/a44132f1-862b-4199-891e-e73fe9fb59f2" />

----------------------------------


# 🚀 Setup & Installation
1. Environment Setup
Clone the repository and install the required Python libraries:

**pip install -r requirements.txt**

Note: Ensure you have torch, torchvision, web3, ipfshttpclient, and streamlit installed.

# 2. Infrastructure Setup (Crucial)
To run the full pipeline, you need two external services running:

**Ganache: Download and start Ganache GUI. Create a workspace on http://127.0.0.1:7545.**

**IPFS: Download IPFS Desktop. Ensure it is started and the API is active on port 5001.**
---------------------------------------------------------------------------------------------------------------------------------------------------
# 🛠️ Execution Steps (Order of Operations)
Follow these steps in order to ensure the project runs correctly:

# Step 1: Train the Model
Train the ResNet18 model on the CIFAR-10 dataset.

**python models/train_cifar.py**
Output: Saves cifar_model.pth in models/saved/

<img width="496" height="865" alt="Screenshot 2026-03-22 145805" src="https://github.com/user-attachments/assets/3bb68a88-ab4f-4d68-abe1-0004633a4fd4" />

----------------------------------------------------------------------------------------------------------------------------------------------------------

# Step 2 : Run Adversarial Attacks
Generate FGSM attacks. This script also uploads images to IPFS and creates local JSON logs.

**python attacks/fgsm_attack.py**

Note: Ensure IPFS Desktop is running before this step.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

<img width="1338" height="656" alt="Screenshot 2026-03-23 175521" src="https://github.com/user-attachments/assets/844ed071-56c4-4182-a959-94bc6a2e039c" />

----------------------------------------------------------------------------------------------------------------------------------------------------------------------

<img width="1151" height="486" alt="Screenshot 2026-03-23 175511" src="https://github.com/user-attachments/assets/e5a25646-78ba-4a1c-bc37-8ec5331ee4b9" />

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




# Step 3: Deploy the Smart Contract
Deploy the AuditNotary.sol contract to your local Ganache blockchain.


**python blockchain/deploy.py**
Output: Generates contract_info.json containing the ABI and Contract Address.

---------------------------------------------------------------------------
<img width="1183" height="135" alt="Screenshot 2026-03-23 175609" src="https://github.com/user-attachments/assets/082c9748-bc53-409b-808d-2d9ec2f48c4f" />

--------------------------------------------------------------------------------------


<img width="1707" height="974" alt="Screenshot 2026-03-23 180723" src="https://github.com/user-attachments/assets/987a0d93-8295-400f-908d-1d48ce889cc1" />

----------------------------------------------------------------------------------------------------

<img width="1919" height="998" alt="Screenshot 2026-03-23 180740" src="https://github.com/user-attachments/assets/90672ff6-a3e1-4e12-a84f-2ed0da541902" />

--------------------------------------------------------------------------------

<img width="1910" height="1000" alt="Screenshot 2026-03-23 180750" src="https://github.com/user-attachments/assets/ec12de4a-48ff-4516-9049-4f92d97e026e" />

-----------------------------------------------------------------------------------------------

<img width="1917" height="1005" alt="Screenshot 2026-03-23 180809" src="https://github.com/user-attachments/assets/1336fb3c-b87d-4473-9e91-9adc64617069" />

-----------------------------------------------------------------------------------

<img width="1919" height="1007" alt="Screenshot 2026-03-23 180819" src="https://github.com/user-attachments/assets/409edb0f-1eb4-40fa-a748-5f2ef0bc513d" />

-----------------------------------------------------------------------------------------------------------------


# Step 4: Blockchain Notarization
Push the generated attack metadata (CIDs) from your local logs to the Ethereum blockchain.

**python blockchain/record_audits.py**

--------------------------------------------------------

<img width="1189" height="784" alt="Screenshot 2026-03-23 175827" src="https://github.com/user-attachments/assets/ba2325cc-4ff5-4218-ae19-8aad8da59ed3" />

------------------------------------------------------

<img width="601" height="647" alt="Screenshot 2026-03-23 175845" src="https://github.com/user-attachments/assets/ccd8d2c1-a477-4148-9bbb-c8237ffb32f1" />

-------------------------------------------------------------------------

# Step 5: Launch the Dashboard
Visualize the results and verify image integrity through the Streamlit UI.


**streamlit run app/dashboard.py**

---------------------------------------------------------------------------------------

<img width="1919" height="882" alt="Screenshot 2026-03-23 175957" src="https://github.com/user-attachments/assets/9948ce17-cf03-4b7c-95e5-e5bfb1003c04" />

----------------------------------------------------------------------------------------------

<img width="1908" height="884" alt="Screenshot 2026-03-23 180010" src="https://github.com/user-attachments/assets/c2759376-243f-4bd5-91f6-1ee65ecc9417" />

------------------------------------------------------------------------------------

<img width="1919" height="886" alt="Screenshot 2026-03-23 180046" src="https://github.com/user-attachments/assets/019c9d0d-5da4-4435-a328-95f8a624211d" />

-------------------------------------------------------------------------------------------

<img width="1900" height="877" alt="Screenshot 2026-03-23 180107" src="https://github.com/user-attachments/assets/079c5852-dfc5-4b44-9d35-1fd2680109d4" />

------------------------------------------------------------------------------------------

<img width="1919" height="891" alt="Screenshot 2026-03-23 180118" src="https://github.com/user-attachments/assets/ede3c2b4-2182-4bb6-b8e8-29bee337ee17" />

-----------------------------------------------------------------------------------------------------

<img width="1894" height="883" alt="Screenshot 2026-03-23 180143" src="https://github.com/user-attachments/assets/2dc414fa-87fd-4af8-8cad-6c7fe6a2196c" />

-----------------------------------------------------------------------------------------------------------

# RESULT

-------------------------------------------------------------------------------

<img width="1907" height="871" alt="Screenshot 2026-03-23 180217" src="https://github.com/user-attachments/assets/8b4b0356-c99d-4b53-9691-79e06a7e7ad1" />

-------------------------------------------------------------------------------------

<img width="1905" height="624" alt="Screenshot 2026-03-23 180239" src="https://github.com/user-attachments/assets/1e28fca9-3b75-40ad-a985-44556a1cc41a" />

---------------------------------------------------------------------------------








