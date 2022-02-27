"""
generate usr badge card
"""

import svglue

from .base import BadgeGnerator
from .base import Images


class UsrBadge(BadgeGnerator):
    template_file = 'templates/base.svg'  

    def __init__(self):
        self.template = svglue.load(file=self.template_file)

    def _set_params(self, params):
        if params.get('format') in ['png']:
            params = self.fix_string_params(params)

        self.template.set_text('usr_fullname', params.get('usr_fullname', 'User'))
        self.template.set_image(
            'usr_img',
            file=Images.get_path('users', params.get('usr_id', 'default')),
            mimetype='image/png'
        )
        self.template.set_image(
            'badge_img',
            file=Images.get_path('badges', params.get('badge_id', 'default')),
            mimetype='image/png'
        )
