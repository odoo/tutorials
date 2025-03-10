from odoo import fields, models

class PosOrder(models.Model):
    _inherit = "pos.order"

    salesperson_id = fields.Many2one("hr.employee", string="Salesperson", help="The Salesperson currently using the Pos Session to sell products")
