from odoo import fields, models


class PosOrder(models.Model):
    _inherit = "pos.order"
    salespersone_id = fields.Many2one("hr.employee")
