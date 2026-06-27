## 1. Project overview

This tutorial repo is a modified Hardhat boilerplate that uses Docker, TypeScript, Viem, and a Vite React dApp to show a complete local Web3 stack. It runs a local Hardhat node in Docker, deploys a token contract with Ignition, and connects a front end through MetaMask to interact with that contract.[1]

## 2. Prerequisites

Ensure the following are installed on your machine before starting:

- Docker Desktop (or Docker Engine + Docker Compose) for running the Hardhat node and associated services.[1]
- Git and a recent Node.js (if you want to run any commands directly inside the containers with `npx`).[1]

## 3. Clone and build containers

From any working directory, clone the repo and build the Docker images:

```bash
git clone https://github.com/jonnymacs/hardhat-tutorial
cd hardhat-tutorial

# Build images defined in docker-compose.yml
docker compose build

# Start all services (Hardhat, dapp, etc.)
docker compose up
```

These commands build and bring up the services defined in `docker-compose.yml`, including a Hardhat environment and the front-end dApp served on port 5173.[1]

## 4. Deploy the Token contract

Open a second terminal, stay in the repository root, and execute into the Hardhat container to deploy the Ignition module:

```bash
cd hardhat-tutorial

docker compose exec hardhat bash

# Inside the container:
npx hardhat ignition deploy ./ignition/modules/Token.ts --network localhost
```

The Ignition deploy command compiles and deploys the `Token` contract to the local Hardhat network exposed by the Docker setup on chain ID 31337.[1]

## 5. Connect MetaMask to local network

With `docker compose up` still running:

1. Open your browser and go to `http://localhost:5173`.  
2. In MetaMask, add a new network:
   - Network name: e.g., `Localhost 31337`  
   - RPC URL: `http://localhost:8545` (or the RPC URL configured in the compose/Hardhat service)  
   - Chain ID: `31337`  
   - Currency symbol: e.g., `ETH`  

This makes MetaMask talk directly to the local Hardhat chain on which the token was deployed, and the dApp at `localhost:5173` will be able to use the connected wallet.[2][1]

## 6. Use the faucet task

After the deployment has succeeded, remain in the second terminal (still inside the Hardhat container) and run the faucet task to mint or transfer test tokens (MMT) to your MetaMask account:

```bash
# Still inside: docker compose exec hardhat bash

# Example: send some MMT to your wallet address
npx hardhat faucet --to <YOUR_METAMASK_ADDRESS> --amount <AMOUNT> --network localhost
```

This custom Hardhat task (`faucet.ts`) sends tokens from a pre-funded account on the local chain to your wallet so you can interact with the dApp (e.g., test transfers or UI flows) without manual token minting steps.[2][1]

## 7. Interact with the dApp

Once your wallet is funded:

- In the dApp UI at `http://localhost:5173`, click “Connect Wallet” and approve the connection in MetaMask to the localhost network you created.[1]
- Use the UI to read balances, send tokens, or trigger contract functions exposed via Viem hooks; each interaction will generate on-chain transactions against your local Hardhat node.[3][1]

This sequence of commands and steps gives a full reproducible workflow from clone to deploy to interact, with `https://github.com/jonnymacs/hardhat-tutorial` as the canonical reference implementation.[1]

[1](https://www.youtube.com/watch?v=8ZMfyZJ2bKk)
[2](https://hardhat.org/hardhat-network)
[3](https://rareskills.io/post/viem-ethereum)