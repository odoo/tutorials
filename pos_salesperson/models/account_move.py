from odoo import models, fields

class AccountMove(models.Model):
    _inherit = "account.move"

    salesperson_id = fields.Many2one(
        "hr.employee", 
        string=" Pos Salesperson", 
        related="pos_order_ids.salesperson_id",
        help="Employee responsible for sale",
    )
