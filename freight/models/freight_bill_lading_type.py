from odoo import models, fields


class FreightBillLadingType(models.Model):
    _name = "freight.bill.lading.type"
    _description = "this is freight type"

    code = fields.Char(string="Code", required=True)
    name = fields.Char(string="Name", required=True)
    status = fields.Boolean(string='Status', default=True)
