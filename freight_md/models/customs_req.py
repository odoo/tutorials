from odoo import models, fields


class CustomsReq(models.Model):
    _name = 'customs.req'
    _description = 'Customs Requests'

    description = fields.Text(string='Description')
    commodity_id = fields.Many2one('commodity', string='Commodity')  # Inverse field
