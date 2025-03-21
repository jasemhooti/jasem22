# Update package list
sudo apt update

# Install required dependencies
sudo apt install software-properties-common -y

# Add deadsnakes PPA for Python versions
sudo add-apt-repository ppa:deadsnakes/ppa -y

# Update package list again
sudo apt update

# Install Python 3.7
sudo apt install python3.7 -y

# Install dependencies for pip
sudo apt install curl python3-distutils -y

# Download and install pip for Python 3.7
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.7 get-pip.py

# Cleanup
rm get-pip.py

# Add pip to PATH (optional)
echo "export PATH=\$PATH:~/.local/bin" >> ~/.bashrc
source ~/.bashrc

# Verify installations
python3.7 --version
pip3 --version
