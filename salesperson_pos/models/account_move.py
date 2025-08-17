from odoo import fields, models

class AccountMove(models.Model):
    _inherit = "account.move"

    salesperson_id = fields.Many2one("hr.employee", string="POS Salesperson", related="pos_order_ids.salesperson_id", store=True, readonly=True)
