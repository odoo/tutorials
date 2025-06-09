from odoo import models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        self.env['account.move'].create({})
        return super().action_sold()
