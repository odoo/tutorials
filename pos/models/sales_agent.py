from odoo import fields, models


class PosOrder(models.Model):
    _inherit = "pos.order"

    sales_agent_id = fields.Many2one(
        comodel_name="hr.employee",
        string="Sales Agent",
        help="Sales agent at the time of billing",
        index=True,
    )
