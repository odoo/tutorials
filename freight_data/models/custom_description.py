from odoo import models, fields


class CustomsDescription(models.Model):
    _name = 'customs.description'
    _description = 'Customs Description'

    description = fields.Text(string='Description')
    description_export = fields.Text(string='Description')
    commodity_data_id = fields.Many2one('commodity.data', string='Commodity Data')
