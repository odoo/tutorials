from odoo import models, fields


class BillOfLadingType(models.Model):
    _name = 'bill.of.lading.type'
    _description = 'Bill Of Lading Type'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    status = fields.Boolean(string='Status', default=True)
