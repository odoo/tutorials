from odoo import api, fields, models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    salesperson_id = fields.Many2one(
        string="Salesperson",
        comodel_name='hr.employee',
    )
