from odoo import models, fields


class MrpProduction(models.Model):
    _inherit = ["mrp.production"]

    order_of_work = fields.Char(string="Order of Work")
