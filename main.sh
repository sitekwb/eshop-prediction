conda create -n eshop-MK-WS python=3.7
conda activate eshop-MK-WS
pip install -r requirements.txt

python 5-server/manage.py runserver &
sleep 10
python 6-abtest-client/abtest-client.py
