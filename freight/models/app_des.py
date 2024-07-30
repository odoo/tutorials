from odoo import models, fields


class AppDes(models.Model):
    _name = 'app.des'
    _description = 'Approval Descriptions'

    description = fields.Char(string='Description')
    commodity_data_id = fields.Many2one('configuration.commodities', string='Commodity')
