# AIFoundryExperiments
Experiments with models in AI Foundry

## Instructions

### Install AZ CLI (Ubuntu)
In case you do not have az installed, follow the instructions here:
```
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```
In depth instructions (if required) are [here](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=apt)

### Login to Az (Choose your developer subscription)
Before you run the code, login to azure by running the command below:
```
az login --tenant 72f988bf-86f1-41af-91ab-2d7cd011db47 --use-device-code
```
You may be prompted to choose a subscription. If so, select:
- 'AIERP_DevPlayground_FinanceCopilot_NonProd' (7999d76d-a4cb-40e9-b3db-73a306deca7f)

Once logged in, Azure AI Foundry client can use your az credentials to get access to all the models you have access to and enable you to run them without API Keys.

### Create a venv and install dependencies
```
git clone https://github.com/akshaybhatnagar-msft/AIFoundryExperiments.git
cd AIFoundryExperiments
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run the code via VS CODE or CLI
```
python src/model-comparisons.py
```
