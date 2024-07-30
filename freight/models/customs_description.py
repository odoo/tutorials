from odoo import models, fields


class CustomsDescription(models.Model):
    _name = 'customs.description'
    _description = 'Customs Descriptions'

    description = fields.Char(string='Description')
    commodity_data_id = fields.Many2one('configuration.commodities', string='Commodity')
