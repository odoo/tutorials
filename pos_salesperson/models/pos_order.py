from odoo import models, fields


class POSEmployee(models.Model):
    _inherit = "pos.order"

    salesperson_id = fields.Many2one('hr.employee', string="SalesPerson")
