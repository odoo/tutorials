from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    accept_one_time = fields.Boolean(
        string="Accept One-Time",
        help="Define if the subscription product can also be bought as a one-time.",
    )
