from flask import Flask, jsonify, render_template, request
import inspect
import json
from collections import defaultdict
from requests import get
from twilio.rest import Client
from os import environ
from threading import Thread

account_sid = environ["TWILIO_ACCOUNT_SID"]
auth_token = environ["TWILIO_AUTH_TOKEN"] 
client_number = environ["TWILIO_NUMBER"]
client = Client(account_sid, auth_token)

app = application = Flask("cryptopticon", static_url_path='')
calls = defaultdict(lambda: 0)
alerts = dict()

@app.route("/cryptopticon", methods=["GET"])
def index():
    calls[inspect.stack()[0][3]] += 1
    return render_template('index.html'), 200


@app.route('/cryptopticon/<string:coin>/alerts/<float:value>/number/<string:number>', methods=['POST'])
def new_alert(coin, value, number):
	with app.app_context():	
		coin = coin.upper()
		if (coin, value, number) in alerts:
			return jsonify({"error": "there is already an alert set up with these parameters"}), 409
		else:
			alerts[(coin, value, number)] = Alert(coin, value, number)
		return '', 201


@app.route('/cryptopticon/<string:coin>/alerts/<float:value>/number/<string:number>', methods=['GET'])
def get_alert(coin, value, number):
	with app.app_context():	
		coin = coin.upper()
		if (coin, value, number) in alerts:
			return jsonify(alerts[(coin, value, number)].status()), 200
		else:
			return jsonify({"error": "no alert found with these parameters"}), 404


@app.route("/cryptopticon/healthz", methods=["GET"])
def healthz():
    calls[inspect.stack()[0][3]] += 1
    return Health(calls) \
               .to_json(), 200


class Health(object):

    def __init__(self, calls):
        self.calls = calls

    def to_json(self):
        return jsonify({
            "requestsServed": {
                "index": self.calls["index"],
                "new_alert": self.calls["net_alert"],
                "get_alert": self.calls["get_alert"],
                "healthz": self.calls["healthz"]
            },
            "status": "healthy"
        })


class Alert(object):
	
	def __init__(self, coin, value, number):
		self.coin = coin
		self.value = value
		self.number = number
		self.current_value = None
		self.monitor_thread = Thread(target=self.monitor)
		self.monitor_thread.start()	

	def monitor(self):
		while True:
			price = self.get_current_price()
			self.current_value = price[self.coin]
			if self.current_value < value:
				self.send_alert()
			sleep(60)
	
	def status(self):
		return self.monitor_thread.isAlive()

	def send_alert(self):
		message = client.api.account.messages.create(to=self.number,
                                             from_=client_number,
                                             body="ALERT: " + self.coin + " has dropped below " + self.value + "!")

	def get_current_price(self):
		with app.app_context():
			return json.loads(get('https://min-api.cryptocompare.com/data/price?fsym=' + self.coin + '&tsyms=USD').text)
if __name__ == '__main__':
    app.run(debug=True)


