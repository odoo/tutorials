from odoo import models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def sell_property(self):
        print("Oui j'ai print là")
        return super().sell_property()
