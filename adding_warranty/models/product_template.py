from odoo import fields, models


class product_template(models.Model):
    _inherit = "product.template"

    is_warranty_available = fields.Boolean(string="Is Warranty Available")
    warranty_id = fields.Many2one("warranty.configuration",string="Select Warranty")
