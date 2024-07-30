from odoo import fields, models


class FreightData(models.Model):
    _name = "freight.data"
    _description = "Freight Data Model"

    code = fields.Char("Code")
    name = fields.Char("Name")
    status = fields.Boolean(string="Status", default=True)
