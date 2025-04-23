from odoo import models, fields

class EstateProperty(models.Model):
    _inherit="estate_property"

    def mark_as_sold(self):
        print("___________________________________________________________________________________________")
        return super().mark_as_sold()
