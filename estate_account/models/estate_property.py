from odoo import models

class EstatePropert(models.Model):
    _inherit = "estate.property"

    def action_set_property_sold(self):
        return super().action_set_property_sold()