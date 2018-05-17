from chalice import Chalice
import requests

app = Chalice(app_name='meditation-cop')


@app.route('/')
def index():
    headers = {'Content-type': 'application/json'}
    print(headers)
    r = requests.post("https://hooks.slack.com/services/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", json={"text":"Automated message : Sound-cloud url goes here"}, headers=headers)
    print(r)
    return {'hello': 'world'}


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
