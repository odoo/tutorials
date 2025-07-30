from odoo import api,fields,models

class PosOrder(models.Model):
    _inherit='pos.order'

    salesperson_id = fields.Many2one("hr.employee", string="Salesperson" , help="employee resposnible for sale")
