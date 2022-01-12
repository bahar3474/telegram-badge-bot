import requests
import shutil


def render_badge(user_fullname, user_id, badge_id):
    scale = 2
    link = 'http://badge_generator:7070'
    encouragement_sentence = ''

    url = '{}/badge?format=png&usr_fullname={}&usr_id={}&badge_id={}&scale={}' \
          '&encouragement_sentence={}'
    badge_url = url.format(
        link,
        user_fullname,
        user_id,
        badge_id,
        scale,
        encouragement_sentence,
    )
    response = requests.get(badge_url, stream=True)
    with open(f'generated_badges/{user_id}_{badge_id}_badge.png', 'wb') \
            as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    return f'generated_badges/{user_id}_{badge_id}_badge.png'
