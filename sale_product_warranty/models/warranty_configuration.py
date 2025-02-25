from odoo import api, fields, models

class WarrantyConfiguration(models.Model):
    _name = "warranty.configuration"
    _description = "Shows warranty for all the products"

    name = fields.Char(string="Name", required=True)
    period = fields.Integer(string="Period(in year)", default="1")
    product_id = fields.Many2one("product.product", string="Product", required=True)
    percentage = fields.Float(string="Percentage %", help="Price of warranty is Percentage of product price", required=True)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if record.product_id:
                record.product_id.sale_ok = False
                record.product_id.purchase_ok = False
                record.product_id.type = "service"
        return records
