from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_kit = fields.Boolean()
    subproduct_ids = fields.One2many('product.subproduct.line', 'product_tmpl_id')

    def _recompute_kit_list_price(self):
        for tmpl in self:
            if tmpl.is_kit and tmpl.subproduct_ids:
                tmpl.list_price = sum(
                    sub.price_unit * sub.kit_unit_qty
                    for sub in tmpl.subproduct_ids
                )

    @api.onchange('subproduct_ids')
    def _onchange_subproduct_ids(self):
        if self.is_kit and self.subproduct_ids:
            self.list_price = sum(
                sub.price_unit * sub.kit_unit_qty
                for sub in self.subproduct_ids
            )
