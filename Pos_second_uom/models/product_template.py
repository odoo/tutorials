from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    pos_secondary_uom_id = fields.Many2one(
        'uom.uom',
        string="POS Secondary UoM",
        help="Optional secondary unit of measure to be used in Point of Sale."
    )
