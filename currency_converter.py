from flask import Flask
from bs4 import BeautifulSoup
import requests
from flask import request, render_template

app = Flask(__name__)


def get_options():
    url = "https://www.xe.com/currencyconverter/convert"
    r = requests.get(url)
    raw_html = r.text
    crawled_data = BeautifulSoup(raw_html, 'html.parser')
    option_dict = {}
    for option in crawled_data.find_all("option"):
        option_dict.update({option.attrs['value']: option.string})
    return option_dict


options_dict = get_options()


@app.route('/', methods=['GET', 'POST'])
def currency_converter():
    if request.method == 'POST':
        result = convert(request.form['amount'], request.form['from_currency'], request.form['to_currency'])
        return render_template('home_page.html', options=options_dict, result=result)
    return render_template('home_page.html', options=options_dict, result=None)


def convert(amount, from_currency, to_currency):
    url = "https://www.xe.com/currencyconverter/convert/?Amount={}&From={}&To={}".format(amount, from_currency,
                                                                                         to_currency)
    r = requests.get(url)
    raw_html = r.text
    crawled_data = BeautifulSoup(raw_html, 'html.parser')
    result = {'result_amount': crawled_data.find("span", {"class": "uccResultAmount"}).string,
              'result_unit': crawled_data.find("span", {"class": "uccResultUnit"}).string,
              'inverse_result_unit': crawled_data.find("span", {"class": "uccInverseResultUnit"}).string,
              'result_time': crawled_data.find("span", {"class": "resultTime"}).string}
    return result
