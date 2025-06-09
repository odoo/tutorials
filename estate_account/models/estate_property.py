from odoo import models


class EstateProperty(models.Model):
    _inherit = "estate.property"
    _description = "Real Estate Property"

    def action_sold(self):
        return super().action_sold()
