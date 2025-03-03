from odoo import api, fields, models


class PosOrder(models.Model):
    _inherit = "pos.order"

    salesperson_id = fields.Many2one(
        comodel_name="hr.employee",
        string="Salesman",
        help="Employee who is at Sales"
    )
