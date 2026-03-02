set -e
python3 -m pip install --upgrade pip
python3 -m pip install torch==2.1.0 --extra-index-url https://download.pytorch.org/whl/cu118
python3 -m pip install -r requirements.txt
echo "GPU installation complete."