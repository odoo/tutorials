from odoo import models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold_offer(self):
        return super().action_sold_offer()
