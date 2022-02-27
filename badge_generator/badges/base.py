import os

import cairosvg
from bidi import algorithm as bidialg
import arabic_reshaper as ar

class BadgeGnerator(object):
    def render(self):
        raise NotImplementedError

    def _fix_string(self, text):
        if not isinstance(text, str):
            return text
        return u' '.join(
            reversed(
                [
                    bidialg.get_display(ar.reshape(word))
                                                    for word in text.split()
                ]
            )
        )

    def fix_string_params(self, params):
        fixed_params = {}
        for key in params:
            fixed_params[key] = self._fix_string(params[key])
        return fixed_params
    
    def _render_image(self, params):
        format = params.get('format', 'svg')
        scale = float(params.get('scale', 1.0))

        svg = self.template.__str__()
        if format == 'svg':
            return svg, 'image/svg+xml'
        if format == 'png':
            return cairosvg.svg2png(bytestring=svg, dpi=scale*100), 'image/png'
        if format == 'pdf':
            return cairosvg.svg2pdf(bytestring=svg), 'application/pdf'
        if format == 'ps':
            return cairosvg.svg2ps(bytestring=svg), 'application/ps'
        return svg, 'image/svg+xml'

    def _set_params(self, params):
        raise NotImplementedError

    def render(self, params):
        self._set_params(params)
        return self._render_image(params)


class Images(object):
    @staticmethod
    def get_path(itype, id):
        image_path = 'images/{}/{}'.format(itype, id)
        if not os.path.exists(image_path):
            image_path = 'images/{}/{}'.format(itype, 'default.png')
        return image_path
