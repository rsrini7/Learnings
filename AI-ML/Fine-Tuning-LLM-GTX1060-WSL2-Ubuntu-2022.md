# Fine-Tuning LLMs with NVIDIA GTX 1060 on WSL2 Ubuntu 20.04

This guide outlines the steps for setting up an environment to fine-tune Large Language Models (LLMs) using an NVIDIA GTX 1060 GPU within WSL2 (Windows Subsystem for Linux) running Ubuntu 20.04.

## 1. Python Version Considerations

*   **Ubuntu 20.04:** Default Python 3.8. Requires `pyenv` for higher Python versions.
*   **Ubuntu 24.04:** Default Python 3.12. PyTorch does not currently provide prebuilt wheels for Python 3.12 (cp312) via the official website or PyPI.
*   **Ubuntu 22.04:** Default Python 3.10. This version is recommended for compatibility.

## 2. WSL2 and Ubuntu 22.04 Setup

1.  Install Ubuntu 22.04 in WSL2:
    ```bash
    wsl --install -d Ubuntu-22.04
    ```
2.  Set Ubuntu 22.04 as the default WSL distribution:
    ```bash
    wsl --setdefault Ubuntu-22.04
    ```
3.  Install `pip` and `venv`:
    ```bash
    sudo apt install python3-pip
    sudo apt install python3-venv
    ```
4.  Install `pipx` and `uv` (a fast Python package installer):
    ```bash
    sudo pip install pipx
    pipx install uv
    ```

## 3. CUDA Toolkit Installation (for WSL-Ubuntu)

Follow these steps to install CUDA Toolkit 12.6 for WSL-Ubuntu:

1.  Download the CUDA repository pin and installer:
    ```bash
    wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin
    sudo mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600
    wget https://developer.download.nvidia.com/compute/cuda/12.6.0/local_installers/cuda-repo-wsl-ubuntu-12-6-local_12.6.0-1_amd64.deb
    ```
2.  Install the repository package and update apt:
    ```bash
    sudo dpkg -i cuda-repo-wsl-ubuntu-12-6-local_12.6.0-1_amd64.deb
    sudo cp /var/cuda-repo-wsl-ubuntu-12-6-local/cuda-*-keyring.gpg /usr/share/keyrings/
    sudo apt-get update
    ```
3.  Install the CUDA toolkit:
    ```bash
    sudo apt-get -y install cuda-toolkit-12-6
    ```
4.  Add CUDA to your PATH and LD_LIBRARY_PATH (add these to your `~/.bashrc` or `~/.profile`):
    ```bash
    export PATH=/usr/local/cuda-12.6/bin:$PATH
    export LD_LIBRARY_PATH=/usr/local/cuda-12.6/lib64:$LD_LIBRARY_PATH
    export PATH="/usr/bin:$PATH"
    export PATH="$HOME/.local/bin:$PATH"
    ```
5.  Verify CUDA installation:
    ```bash
    nvcc --version
    nvidia-smi
    ```

## 4. Python Environment and Libraries

1.  Create and activate a Python virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
    *Note: If you used `uv` for `pipx`, ensure you use `uv pip install` instead of `pip install` within your virtual environment.*

2.  Install PyTorch with CUDA 11.8 support (adjust CUDA version if needed):
    ```bash
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    ```
3.  Verify PyTorch CUDA availability:
    ```bash
    python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
    ```
4.  Install common data science and LLM-related libraries:
    ```bash
    pip install scikit-learn matplotlib pandas jupyterlab notebook
    pip install transformers peft bitsandbytes accelerate
    ```

## 5. Unsloth Compatibility with GTX 1060

**Important Note:** The NVIDIA GTX 1060 is **not officially supported** by Unsloth for GPU acceleration.

*   Unsloth requires a minimum CUDA Compute Capability of 7.0.
*   The GTX 1060 only provides Compute Capability 6.1.
*   Attempts to use Unsloth with a GTX 1060 will result in errors from Triton or PyTorch kernels, such as:
    ```
    Triton only supports devices of CUDA Capability >= 7.0, but your device is of CUDA capability 6.1
    ```
*   Supported GPUs for Unsloth start from GTX 1070 and later (Volta, Turing, Ampere, Ada, and Blackwell architectures).

Therefore, while you can set up the environment, Unsloth will not leverage the GPU on a GTX 1060 for accelerated fine-tuning.