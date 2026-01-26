from odoo import models

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sell(self):
        print('----- INHERITED -----')
        return super().action_sell()
