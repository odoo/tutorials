# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    first_uom_category_id = fields.Many2one(comodel_name='uom.category', related='uom_id.category_id')
    second_uom_id = fields.Many2one(
        comodel_name='uom.uom',
        string="Second Unit Of Measure",
        domain="[('category_id', '=', first_uom_category_id), ('id', '!=', uom_id)]",
        help="List of secondary UOMs that can be used for this product"
    )
    is_use_second_uom = fields.Boolean()


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def _load_pos_data_fields(self, config_id):
        return super()._load_pos_data_fields(config_id) + ['second_uom_id', 'is_use_second_uom']
