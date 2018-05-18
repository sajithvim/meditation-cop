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
            return process_help()
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
    starting_index = raw_request.index('&text=') + 6
    ending_index = raw_request.index('&response_url')
    return raw_request[starting_index:ending_index]


def process_query(query):
    functions_map = {
        "help": process_help,
        "minute": process_minute,
        "schedule": process_schedule,
        "introduction": process_introduction,
        "break": process_break,
    }
    query_words = query.split()
    if query_words is None or len(query_words) < 1:
        return process_help()
    runnable_function = functions_map.get(query_words[0])
    if runnable_function is None:
        return process_help()
    return runnable_function(query)


def process_break():
    url = "https://myob.slack.com/files/U8WA5CRT6/FAR9EPPEU/Mini_Break_Reminder"

    return generate_response(get_multimedial_url(url, "Take a break"))


def process_introduction(query):
    url = "https://www.youtube.com/watch?v=w6T02g5hnT4"
    response_content = get_multimedial_url(url, "Introduction to meditation")
    return generate_response(response_content)


def get_multimedial_url(url, title):
    response_content = {
        "parse": "full",
        "response_type": "in_channel",
        "unfurl_media": True,
        "unfurl_links": True,
        "text": url,
        "attachments": [
            {
                "title": title,
                "image_url": url,
                "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQPgFSdJB9qPd87KHD_4sIeoyLZiqhdGcuTvA7bjoGMC91EUuAB",
                "fields": [
                    {
                        "title": "Priority",
                        "value": "High",
                        "short": False
                    }
                ],
                "text": ""
            }
        ],
    }
    return response_content


def process_help(query=None):
    help_text = {
        "response_type": "in_channel",
        "text": "*schedule* [interval] : helps you to schedule a meditation session. Eg: schedule 1 hour \n "
        + "*minute* : sets your environment for one minute meditation \n"
        + "*introduction* : introduces the meditation. A basic overview of the benefits etc."
    }
    return generate_response(help_text)


def process_minute(query):
    url = get_random_clip_url()
    response_content = {
        "parse": "full",
        "response_type": "in_channel",
        "unfurl_media": True,
        "unfurl_links": True,
        "text": url,
        "attachments": [
            {
                "title": " To play the one minute meditation please click on the link above.",
                "image_url": url,
                # "thumb_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQPgFSdJB9qPd87KHD_4sIeoyLZiqhdGcuTvA7bjoGMC91EUuAB",

            }
        ],
    }
    return generate_response(response_content)


def process_schedule(query):
    response_content = {
        "response_type": "in_channel",
        "text": "/polly \"When should we hold the meeting?\" \"9am\"\"10am\" \"11am\" ",
    }
    return generate_response(response_content)


def process_random_clip():
    url = get_random_clip_url()
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

# https://soundcloud.com/amr-reda-1/relax-my-mind


def get_sountract_data():
    sound_map = [
        "https://myob.slack.com/files/U8WA5CRT6/FASSCB18W/just-a-minute-relaxation-space_for_quietness.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FARNUDN5S/just-a-minute-relaxation-relaxing_my_mind.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FAS45RAG5/just-a-minute-relaxation-relaxing.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FASSC9HQW/just-a-minute-relaxation-mental_oxygen.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FAS45PXB7/just-a-minute-relaxation-breathing_calm.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FARSLHQBD/just-a-minute-relaxation-being_relaxed.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FAR91M6M6/just-a-minute-concentration-focusing_my_thoughts.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FAR91MN48/just-a-minute-concentration-focusing_thought.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FAS03RUG2/just-a-minute-concentration-plugging_in.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FAT1HC6UX/just-a-minute-concentration-positive_focus.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FARSLAFFV/just-a-minute-concentration-slow_food.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FASSC1YES/just-a-minute-concentration-transformative_focus.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FAR92S7C0/just-a-minute-silence-being_myself.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FARDJVBFB/just-a-minute-silence-creating_inner_space.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FAR92T6C8/just-a-minute-silence-inner_light.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FAR92TL3S/just-a-minute-silence-the_art_of_silence.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FAT1JHEFR/just-a-minute-silence-the_mirror.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FARNVF6BE/just-a-minute-visualisation-freedom.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FARNVFK3N/just-a-minute-visualisation-letting_go.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FARSMMJQ3/just-a-minute-visualisation-rising_above.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FASSDCU8N/just-a-minute-visualisation-the_forest.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FAT1JPQP9/just-a-minute-visualisation-the_kaleidoscope_of_life.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FARNVGM1A/just-a-minute-visualisation-unlimited_possibilities.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FAR93NBCG/just-a-minute-sharing-availability.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FASSE3PEJ/just-a-minute-sharing-bringing_light.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FAS47JMKP/just-a-minute-sharing-catalyst.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FARSNDCN7/just-a-minute-sharing-generosity.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FARSNDSDR/just-a-minute-sharing-moments_of_peace.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FAT1KG7HD/just-a-minute-sharing-positive_influence.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FAS06PGSW/just-a-minute-meditation-a_clear_mind.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FAS48E7QV/just-a-minute-meditation-feeling_safe.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FARNX3VRA/just-a-minute-meditation-point_of_focus.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FAR94NY3A/just-a-minute-meditation-remembering.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FAT1LCPQF/just-a-minute-meditation-self-esteem.mp3",
        "https://myob.slack.com/files/U8WA5CRT6/FARNX55K6/just-a-minute-meditation-the_true_self.mp3",

    ]
    return sound_map


def find_rand_url(data, rand_number):
    print("rand-number", rand_number)
    return data[rand_number]
