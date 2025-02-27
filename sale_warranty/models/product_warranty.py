# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductWarranty(models.Model):
    _name = "product.warranty"
    _description = "Product Warranty"

    name = fields.Char(string="Name", required=True)
    duration = fields.Integer(string="Duration (Years)", required=True, help="The duration of the warranty in years.")
    percent = fields.Float(string="Warranty Price Percentage", required=True,
                           help="Percentage of the product price that will be charged as the warranty price.")
    product_id = fields.Many2one(comodel_name="product.product", string="Product", required=True)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            record.product_id.sale_ok = False
            record.product_id.purchase_ok = False
            record.product_id.type = "service"
        return records
