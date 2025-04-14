from odoo import fields, models


class PosOrderInherit(models.Model):
    _inherit = "pos.order"

    salesperson_id = fields.Many2one("hr.employee", string="SalesPerson")
