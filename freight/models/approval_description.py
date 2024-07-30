from odoo import models, fields


class ApprovalDescription(models.Model):
    _name = 'approval.description'
    _description = 'Approval Descriptions'

    description = fields.Char(string='Description')
    commodity_data_id = fields.Many2one('configuration.commodities', string='Commodity')
