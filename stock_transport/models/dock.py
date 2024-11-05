from odoo import fields, models


class Dock(models.Model):
    _name = "stock.transport.dock"
    _description = "Stock Transport Dock Model."

    name = fields.Char("Dock")
