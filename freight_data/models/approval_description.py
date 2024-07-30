from odoo import models, fields


class ApprovalDescription(models.Model):
    _name = 'approval.description'
    _description = 'Approval Description'

    description = fields.Text(string='Description')
    description_export = fields.Text(string='Description')
    commodity_data_id = fields.Many2one('commodity.data', string='Commodity Data')
