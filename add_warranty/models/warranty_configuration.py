from odoo import fields, models

class WarrantyConfiguration(models.Model):
    _name = "warranty.configuration"
    _description = "Add warranty for products"

    name = fields.Char(string = "Name", required = True)
    duration = fields.Integer(string = "Duration (in Years)")
    percentage = fields.Float(string = "Percentage", required = True)
    product_id = fields.Many2one('product.template', domain = [("type", "=", "service")], string = "Product", ondelete="cascade", required=True)

    _sql_constraints = [
        ("unique_warranty_configuration", "UNIQUE(name, product_id)", "Warranty configuration already exists"),
        ("valid_percentage", "CHECK(percentage > 0)", "Percentage must be greater than zero"),
        ("valid_duration", "CHECK(duration > 0)", "Warranty duration must be greater than zero")
    ]