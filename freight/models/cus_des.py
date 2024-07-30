from odoo import models, fields


class CusDes(models.Model):
    _name = 'cus.des'
    _description = 'Approval Descriptions'

    description = fields.Char(string='Description')
    commodity_data_id = fields.Many2one('configuration.commodities', string='Commodity')
