from odoo import models, fields


class FreightType(models.Model):
    _name = "freight.type"
    _description = "Freight Type"

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    status = fields.Boolean(string='Status')
