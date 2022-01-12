import shutil

import requests

def render_badge(
        link,
        usr_fullname,
        usr_id,
        badge_id,
        scale,
        encouragement_sentence='',
):
    url = '{}/badge?format=png&usr_fullname={}&usr_id={}&badge_id={}&scale={}&encouragement_sentence={}'
    badge_url = url.format(
        link,
        usr_fullname,
        usr_id,
        badge_id,
        scale,
        encouragement_sentence,
    )
    response = requests.get(badge_url, stream=True)
    with open(f'generated_badges/{usr_id}_badge.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    return 


if __name__ == '__main__':

    render_badge(
            link='http://badge_generator:7070',
            usr_fullname='قلی‌چه',
            usr_id='',
            badge_id='',
            scale=2
    )
