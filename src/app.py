import flask
from service import Fact
from service.trivia import TriviaService
from service.exchange import ExchangeService

import config

facts = [Fact('Toyota sold {total_value} cars in this time globally!', 32, 10),
         Fact(u'You have collectively been exposed to {total_value}\u00b5Sv of radiation during this time!', 0.345, 3600),
         Fact('Crossrail will have tunnelled {total_value}mm in this time!', 9.92, 60),
         Fact(u'On minimum wage you\'d all have earned \u00a3{total_value} in this time!', 6.50, 3600),
         Fact('You could all have brewed {total_value} cups of tea in this time!', 1, 180),
         Fact('{number_of_attendees} AdFuser developers could have written {total_value} lines of code in this time!', 7, 3600),
         Fact('You {number_of_attendees} could have downloaded {total_value} MP3\'s on the average home broadband line in this time!', 1, 77)
         ]

class ReturnStatus(object):
    error = 'Error'
    ok = 'OK'

RETURN_TEMPLATE = {
        'status': ReturnStatus.ok,
        'type': 'actual',
        'trivia': [],
    }

app = flask.Flask('mandayclock', static_url_path='/static')

@app.route('/')
def i_dont_even_know():
    # like this while i dev
    return app.send_static_file('front.html')
#     return flask.render_template('index.html', stuff=[1, 'poo', False])

@app.route('/trivia')
def i_probably_know_some_stuff():
    res = RETURN_TEMPLATE

    attendees = flask.request.args.get('number_of_attendees', 0)
    elapsed_seconds = int(float(flask.request.args.get('elapsed_seconds', 0)))

    if not attendees or not elapsed_seconds:
        res['status'] = ReturnStatus.error
        return flask.jsonify(**res)
    try:
        attendees, elapsed_seconds = int(attendees), int(elapsed_seconds)
    except:
        res['status'] = ReturnStatus.error
        return flask.jsonify(**res)

    trivia = TriviaService(facts, attendees, elapsed_seconds)
    res['trivia'] = trivia.get_facts(2)

    return flask.make_response(flask.jsonify(**res),
        500 if res['status'] == 'Error' else 200)

@app.route('/ex_trivia', methods=['POST'])
def i_definitely_know_all_the_stuff():
    res = RETURN_TEMPLATE
    username = flask.request.args.get('username', '')
    password = flask.request.args.get('password', '')

    if not username or not password:
        res['status'] = ReturnStatus.error
        return flask.jsonify(**res)

    ex = ExchangeService(config.EXCHANGE_DOMAIN, config.EXCHANGE_URL)
    ex.connect(username, password)
    events = ex.list_events()

    return flask.jsonify(**res)

if __name__ == "__main__":
    app.run(debug=True)
