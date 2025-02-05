from odoo import fields, models


class Partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    target_sales_won = fields.Integer('Won in Opportunities Target')
    target_sales_done = fields.Integer('Activities Done Target')
    