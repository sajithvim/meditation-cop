from chalice import Chalice, Response
import requests
import random

app = Chalice(app_name='meditation-cop')


@app.route('/', methods=['POST', 'GET'], content_types=['application/x-www-form-urlencoded', 'application/json'])
def invoke_api():
    try:
        print(app.current_request)
        request = app.current_request
        print('raw-request', request.raw_body)
        query = decode_query(request.raw_body.decode("utf-8"))
        print('query', query)
    except Exception as e:
        print(e)
    return invoke()


@app.schedule('rate(20 minutes)')
def invoke_scheduler(args):
    return invoke()


def decode_query(raw_request):
    print(raw_request)
    starting_index = raw_request.index('&text=') + 6
    print('starting_index', starting_index)
    ending_index = raw_request.index('&response_url')
    print('ending_index', ending_index)
    return raw_request[starting_index:ending_index]


def invoke():
    print('starting')
    data = get_sountract_data()
    rand_number = random.randint(1, len(data))
    url = find_rand_url(data, rand_number)
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    r = requests.post("https://hooks.slack.com/services/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",
                      json={"text": "content:" + url}, headers=headers)
    response = {
        "response_type": "in_channel",
        "text": url,
        "attachments": [
            {
                "text": url
            }
        ]
    }
    output = Response(body=response,
                      status_code=200,
                      headers={'Content-Type': 'application/json'})
    return output


def get_sountract_data():
    sound_map = {
        "concentration": "https://files.slack.com/files-pri/T02998537-FAR210MGU/download/relaxing_my_mind.mp3",
        "connecting": "https://files.slack.com/files-pri/T02998537-FAR210MGU/download/relaxing_my_mind.mp3",
        "relaxation": "https://files.slack.com/files-pri/T02998537-FAR210MGU/download/relaxing_my_mind.mp3",
    }
    return sound_map


def find_rand_url(data, rand_number):
    count = 0
    for item, url in data.items():
        if count == rand_number:
            return url
        count = count + 1
    return "https://soundcloud.com/amr-reda-1/relax-my-mind"
