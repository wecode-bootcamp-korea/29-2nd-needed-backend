# !/bin/sh

# create conda virtual environment
echo y | conda create -n needed_release python=3.9 && conda activate needed_release

# install dependency packages
pip install -r requirements.txt

# find server IP Address
echo "15.165.203.121"
echo  | ipconfig getifaddr en0

# runserver
python manage.py runserver 0:8080
