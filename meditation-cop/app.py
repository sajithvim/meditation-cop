from chalice import Chalice, Response
import requests
import random

app = Chalice(app_name='meditation-cop')


@app.route('/', methods=['POST', 'GET'], content_types=['application/x-www-form-urlencoded', 'application/json'])
def invoke_api():
    try:
        request = app.current_request
        query = decode_query(request.raw_body.decode("utf-8"))
        if query is None:
            return process_random_clip()
        return process_query(query)
    except Exception as e:
        print(e)


@app.schedule('rate(2 minutes)')
def invoke_scheduler(args):
    try:
        sound_url = get_random_clip_url()
        post_message_to_slack(sound_url)
    except Exception as e:
        print(e)


def decode_query(raw_request):
    print(raw_request)
    starting_index = raw_request.index('&text=') + 6
    print('starting_index', starting_index)
    ending_index = raw_request.index('&response_url')
    print('ending_index', ending_index)
    return raw_request[starting_index:ending_index]


def process_query(query):
    functions_map = {
        "help": process_help,
        "minute": process_minute,
        "schedule": process_schedule,
    }
    query_words = query.split()
    if query_words is None or len(query_words) < 1:
        return process_random_clip()
    runnable_function = functions_map.get(query_words[0])
    if runnable_function is None:
        return process_random_clip()
    return runnable_function(query)


def process_help(query):
    help_text = {
        "response_type": "in_channel",
        "text": "*schedule* : helps you to schedule a meditation session \n *minute* : Sets your environment for one minute meditation \n"
    }
    return generate_response(help_text)


def process_minute(query):
    item, url = get_random_clip_url()
    response_content = {
        "response_type": "in_channel",
        "text": url,
        "attachments": [
            {
                "title": item + " music for meditation",
                "image_url": url,
                "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQPgFSdJB9qPd87KHD_4sIeoyLZiqhdGcuTvA7bjoGMC91EUuAB",
                "fields": [
                    {
                        "title": "Priority",
                        "value": "High",
                        "short": False
                    }
                ],
                "text": "Sample material tp aid meditation"
            }
        ],
    }
    return generate_response(response_content)


def process_schedule(query):
    response_content = {
        "response_type": "in_channel",
        "text": "/polly survey ",
    }
    return generate_response(response_content)


def process_random_clip():
    item, url = get_random_clip_url()
    response_content = {
        "unfurl_media": True,
        "text": url,
    }
    return generate_response(response_content)


def generate_response(content):
    response = Response(body=content,
                        status_code=200,
                        headers={'Content-Type': 'application/json'})
    return response


def post_message_to_slack(content):
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    r = requests.post("https://hooks.slack.com/services/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",
                      json={"text": "content:" + url}, headers=headers)


def get_random_clip_url():
    data = get_sountract_data()
    rand_number = random.randint(1, len(data))
    return find_rand_url(data, rand_number)


def get_sountract_data():
    sound_map = {
        "concentration": "https://soundcloud.com/amr-reda-1/relax-my-mind",
        "connecting": "https://soundcloud.com/amr-reda-1/relax-my-mind",
        "relaxation": "https://soundcloud.com/amr-reda-1/relax-my-mind",
    }
    return sound_map


def find_rand_url(data, rand_number):
    count = 0
    for item, url in data.items():
        if count == rand_number:
            return item, url
        count = count + 1
    return 'concentration', data['concentration']
