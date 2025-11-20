from odoo import models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_mark_as_sold(self):
        return super().action_mark_as_sold()
