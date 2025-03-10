from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    custom_price = fields.Float('Custom Price', digits='Product Price')
    min_price = fields.Float('Min Price', digits='Product Price')


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _load_pos_data_fields(self, config_id):
        fields = super()._load_pos_data_fields(config_id)
        fields.extend(['custom_price', 'min_price'])
        return fields
