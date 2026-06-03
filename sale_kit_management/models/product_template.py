from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_kit = fields.Boolean()
    subproduct_ids = fields.One2many('product.subproduct.line', 'product_tmpl_id')

    @api.depends('is_kit', 'subproduct_ids.price_unit', 'subproduct_ids.kit_unit_qty')
    def _compute_kit_list_price(self):
        for product in self:
            if product.is_kit and product.subproduct_ids:
                product.list_price = sum(
                    sub.price_unit * sub.kit_unit_qty
                    for sub in product.subproduct_ids
                )

    @api.onchange('subproduct_ids')
    def _onchange_subproduct_ids(self):
        if self.is_kit and self.subproduct_ids:
            self.list_price = sum(
                sub.price_unit * sub.kit_unit_qty
                for sub in self.subproduct_ids
            )
