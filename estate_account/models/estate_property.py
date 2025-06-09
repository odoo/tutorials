from odoo import models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        return super().action_sold()
