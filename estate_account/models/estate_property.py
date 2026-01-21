from odoo import fields, models

class EstateProperty(models.Model):
    _inherit = ["estate.property"]

    def sell_property(self):
        print("WORKING")
        return super().sell_property()
