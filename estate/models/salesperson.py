from odoo import fields, models


class Salesperson(models.Model):
    _name = 'salesperson'
    _description = 'The individual handling the sales for the estate'

    name = fields.Char('Salesperson')
