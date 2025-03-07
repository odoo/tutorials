# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class PosOrder(models.Model):
    _inherit = "pos.order"

    salesperson_id = fields.Many2one(string="Salesperson", comodel_name="hr.employee")
