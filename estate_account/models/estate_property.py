from odoo import fields, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self):
        return super().action_sold_property()
