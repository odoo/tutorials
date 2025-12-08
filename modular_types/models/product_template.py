from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    modular_type_ids = fields.Many2many(
        'modular.type.config',
        'component_product_id',
        string='Modular Types',
        help="Select the modular types applicable to this product template."
    )
