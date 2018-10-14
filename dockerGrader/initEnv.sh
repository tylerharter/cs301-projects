sudo apt-get install rabbitmq-server
python3 -m venv venv && . venv/bin/activate && pip install wheel && pip install -r requirements.txt && deactivate && echo "Success!"
