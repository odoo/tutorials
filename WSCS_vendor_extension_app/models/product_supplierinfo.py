from odoo import models, fields


class ProductSupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    qty_per_case = fields.Integer(string="Quantity per Case")
    cases_per_container = fields.Integer(string="Cases per Container")
    price_per_1000 = fields.Float(string="Cost per 1000")
    incoterm_id = fields.Many2one(
        "account.incoterms",  # this is the incoterms model in Odoo
        string="Incoterms",
    )
    product_status_id = fields.Many2one(
        related="product_tmpl_id.product_status_id", string="Product Status", store=True
    )
