from odoo import fields, models

class ApprovalCategory(models.Model):
    _inherit = 'approval.category'

    from_amount = fields.Monetary("From Amount")
    to_amount = fields.Monetary("To Amount")
    currency_id = fields.Many2one("res.currency", string="Currency")
    is_sales_approval = fields.Boolean("Is Sales Order Approval?")
