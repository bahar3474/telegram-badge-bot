import requests


def check_id_and_save_image(telegram_id, bot_token, path):
    r = requests.post(url=f'https://api.telegram.org/bot{bot_token}/getUserProfilePhotos',
                      data={'user_id': telegram_id})
    result = r.json()
    if result['ok']:
        last_image_id = result['result']['photos'][0][0]['file_id']
        r2 = requests.post(url=f'https://api.telegram.org/bot{bot_token}/getFile',
                          data={'file_id': last_image_id})

        image_url = f'https://api.telegram.org/file/bot{bot_token}/{r2.json()["result"]["file_path"]}'
        img_data = requests.get(image_url).content
        with open(path, 'wb') as handler:
            handler.write(img_data)
    return True


def overlay(badge_img, image):
    y_offset = 0
    x_offset = image.shape[1] - badge_img.shape[1]
    y1, y2 = y_offset, y_offset + badge_img.shape[0]
    x1, x2 = x_offset, x_offset + badge_img.shape[1]
    alpha_s = badge_img[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s
    for c in range(0, 3):
        image[y1:y2, x1:x2, c] = (alpha_s * badge_img[:, :, c] +
                                  alpha_l * image[y1:y2, x1:x2, c])

    return image
