from odoo import fields, models


class BillOfLadingType(models.Model):
    _name = 'bill.of.lading.type'
    _description = 'Bill of Lading Type'

    code = fields.Char('Code', required=True)
    name = fields.Char('Name', required=True)
    status = fields.Boolean('Active', default=True)
