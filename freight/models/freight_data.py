from odoo import models, fields


class FreightData(models.Model):
    _name = "freight.data"
    _description = "This is freight data"

    name = fields.Char(string='Name', required=True)
