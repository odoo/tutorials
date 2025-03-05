from odoo import api, fields, models


class ProductTypeKitWizard(models.TransientModel):
    _name = 'product.type.kit.wizard'
    _description = "Wizard for Sub Products of Kit Product"

    product_id = fields.Many2one('product.template', string="Kit Product", readonly=True)
    sub_product_ids = fields.One2many('product.type.kit.wizard.line', 'wizard_id', string="Sub Products")

    @api.model
    def default_get(self, fields_list):
        """Auto-fetch product and its sub-products when wizard opens."""
        defaults = super().default_get(fields_list)
        product_id = self.env.context.get('default_product_id')

        if product_id:
            product = self.env['product.template'].browse(product_id)
            defaults['product_id'] = product_id
            sub_product_lines = []

            for sub_product in product.sub_products_ids:
                sub_product_lines.append((0, 0, {
                    'product_id': sub_product.id,
                    'quantity': 1,
                    'price': sub_product.list_price,
                }))

            defaults['sub_product_ids'] = sub_product_lines

        return defaults
