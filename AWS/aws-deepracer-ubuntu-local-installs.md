# AWS DeepRacer Ubuntu Setup with NVIDIA

This guide outlines the steps to set up AWS DeepRacer on Ubuntu with NVIDIA GPU support.

## 1. System Update and NVIDIA Driver Installation

1.  Update and upgrade your system:
    ```bash
    sudo apt update
    sudo apt upgrade
    ```
2.  Check NVIDIA driver status (optional, for verification):
    ```bash
    nvidia-smi
    ```
3.  Install NVIDIA utilities and driver:
    ```bash
    sudo apt install nvidia-utils-515
    sudo apt install nvidia-driver-515
    ```
4.  Select NVIDIA as the primary graphics provider:
    ```bash
    sudo prime-select nvidia
    ```
5.  Reboot your system for changes to take effect:
    ```bash
    sudo reboot
    ```
6.  Verify NVIDIA driver installation after reboot:
    ```bash
    nvidia-smi
    ```

## 2. Docker Installation

1.  Install necessary packages for Docker:
    ```bash
    sudo apt update
    sudo apt-get install ca-certificates curl gnupg lsb-release
    ```
2.  Add Docker's official GPG key:
    ```bash
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    ```
3.  Set up the Docker repository:
    ```bash
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    ```
4.  Update apt package index and install Docker Engine:
    ```bash
    sudo apt update
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
    ```
5.  Add your user to the `docker` group to run Docker commands without `sudo`:
    ```bash
    sudo usermod -aG docker $USER
    ```
6.  Install Docker Compose (if not included with `docker-compose-plugin`):
    ```bash
    sudo apt install docker-compose
    ```
7.  Enable and start Docker services:
    ```bash
    sudo systemctl enable docker.service
    sudo systemctl enable containerd.service
    ```
8.  Reboot your system for group changes to take effect:
    ```bash
    sudo reboot
    ```
9.  Verify Docker installation after reboot:
    ```bash
    docker ps
    ```

## 3. NVIDIA Container Toolkit Installation

1.  Add the NVIDIA Container Toolkit repository:
    ```bash
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
    curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
    ```
2.  Update apt package index and install the toolkit:
    ```bash
    sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
    ```
3.  Restart Docker daemon:
    ```bash
    sudo systemctl restart docker
    ```
4.  Verify NVIDIA GPU access with Docker:
    ```bash
    sudo docker run --gpus all nvidia/cuda:11.0-base nvidia-smi
    ```

## 4. DeepRacer for Cloud Setup

1.  Clone the DeepRacer for Cloud repository:
    ```bash
    sudo apt install git # Ensure git is installed
    git clone https://github.com/aws-deepracer-community/deepracer-for-cloud
    ```
2.  Navigate into the cloned directory:
    ```bash
    cd deepracer-for-cloud/
    ```
3.  Pull the DeepRacer SageMaker GPU image:
    ```bash
    docker pull awsdeepracercommunity/deepracer-sagemaker:5.0.0-gpu
    ```
4.  Initialize the DeepRacer environment:
    ```bash
    bin/init.sh
    ```
5.  Install `jq` (if not already installed):
    ```bash
    sudo apt install jq
    ```
6.  Rea_initialize the environment after `jq` installation:
    ```bash
    bin/init.sh
    ```
7.  Activate the DeepRacer environment:
    ```bash
    source bin/activate.sh
    ```

## 5. AWS CLI and Boto3 Setup

1.  Install AWS CLI:
    ```bash
    sudo apt install awscli
    ```
2.  Install/upgrade boto3 and AWS CLI using pip:
    ```bash
    pip install boto3
    pip install --upgrade awscli
    ```
3.  Configure AWS CLI with a profile (e.g., `minio`):
    ```bash
    aws configure --profile minio
    ```

## 6. Docker Swarm Initialization (Optional)

If you encounter issues with multiple network interfaces, initialize Docker Swarm:
```bash
docker swarm init --advertise-addr 127.0.0.1
```

## 7. Training and Customization

1.  **Edit `deepracer-for-cloud/system.env`**: Change to GPU for the SageMaker image.
2.  **Customize Training**: Modify `hyperparameters.json`, `model_metadata.json`, and `reward_function.py` for better model performance.
3.  **Upload Custom Files**: Before starting training, upload custom files:
    ```bash
    dr-upload-custom-files
    ```
    (This prevents a `404 HeadObject operation: Not Found` error).
4.  **Start Training**: 
    ```bash
    dr-start-training
    ```
    If training appears stuck, open a new terminal, activate the environment (`source bin/activate.sh`), and issue `dr-stop-training`.
5.  **Monitor Training**: If training has started, open `localhost:8080` in your browser and click `kvs_stream` to see live training and evaluation.

## 8. Policy Training Configuration

To run policy training, update the `/etc/docker/daemon.json` file with the following settings:

```json
{
  "runtimes": {
    "nvidia": {
      "path": "nvidia-container-runtime",
      "runtimeArgs": []
    }
  },
  "default-runtime": "nvidia"
}
```

## 9. Stopping and Restarting a Model with a Different Reward Function

To stop a model and restart it with a slightly different reward function without starting from iteration 0:

1.  **Update `run.env` files manually**:
    ```ini
    DR_LOCAL_S3_MODEL_PREFIX=Experiment11c
    DR_LOCAL_S3_PRETRAINED=True
    DR_LOCAL_S3_PRETRAINED_PREFIX=Experiment11b
    ```
2.  **Specify a different reward function file** (assuming you have an actual file with that name in your `custom_files` folder):
    ```ini
    DR_LOCAL_S3_REWARD_KEY=$DR_LOCAL_S3_CUSTOM_FILES_PREFIX/reward_function_returnspeed_exp11b.py
    ```
    *Tip: It's recommended to use a different Python file for each reward function you are testing.*

3.  **Update and Increment Training**:
    ```bash
    dr-update
    dra_increment-training
    ```