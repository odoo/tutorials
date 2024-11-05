from odoo import fields, models


class dock(models.Model):
    _name='dock'

    name = fields.Char(required=True)
