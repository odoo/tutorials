from odoo import fields, models

class ApprovalImportDescription(models.Model):
    _name = 'approval.import.description'
    _description = 'Approval Import Description Model'

    commodity_data_id = fields.Many2one('commodity.data')
    description = fields.Char(string="Description")
