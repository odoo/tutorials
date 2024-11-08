from odoo import fields, models


class Dock(models.Model):
    _name = 'dock.dock'

    name = fields.Char(required=True)
