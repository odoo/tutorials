from odoo import models


class Property(models.Model):
    _inherit = "estate.property"

    def sell(self):
        return super().sell()
