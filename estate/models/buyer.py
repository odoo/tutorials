from odoo import fields, models


class Buyer(models.Model):
    _name = 'buyer'
    _description = 'The entity to buy the estate'

    name = fields.Char('Buyer')
