# models/product_template.py
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    accept_one_time = fields.Boolean(
        string="Accept One-Time",
        help="Allow this subscription product to be sold as a one-time purchase."
    )

