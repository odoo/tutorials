from odoo import models, fields


class Approvals(models.Model):
    _name = 'approvals'
    _description = 'Approvals'

    description = fields.Text(string='Description')
    commodity_id = fields.Many2one('commodity', string='Commodity')  # Inverse field
