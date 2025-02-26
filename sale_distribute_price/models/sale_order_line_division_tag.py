from odoo import fields, models

class SaleOrderLineDivisionTag(models.Model):
    _name = "sale.order.line.division.tag"
    _description = "Sale order division tag"

    name = fields.Float("Name")
