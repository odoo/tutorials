from odoo import models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        # just for testing purpost
        res = super().action_sold()
        print("hello there")

        return res
