from odoo import  fields, models

class Dock(models.Model):
    _name = "dock"
    _description = "Dock of Stock Transport"

    name = fields.Char()