from odoo import fields, models

class PosOrder(models.Model):
    _inherit = "pos.order"

    salesperson_id = fields.Many2one(
        comodel_name = 'hr.employee',
        string = 'Salesperson',
        help = "Salesperson at the time of billing"
    )
