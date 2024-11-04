from odoo import models, fields


class Dock(models.Model):
    _name = 'stock.transport.dock'
    _description = "A model to store Dock"

    name = fields.Char()
