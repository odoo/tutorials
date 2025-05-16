from odoo import api, fields, models


class ProductWarranty(models.Model):
    _name = "product.warranty"
    _description = "Warranties for Product"

    year = fields.Integer(string="Warranty Period (Years)", required=True)
    name = fields.Char(string="Warranty Name", required=True)
    percentage = fields.Float(string="Warranty Percentage", required=True)
    product_id = fields.Many2one("product.product", string="Product", required=True)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            record.product_id.sale_ok = False
            record.product_id.purchase_ok = False
            record.product_id.type = "service"
        return records
