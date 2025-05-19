from odoo import fields, models


class ProductWarrantyConfiguration(models.Model):
    _name = "product.warranty.configuration"
    _description = "Manages product warranties"
    
    _sql_constraints = [
        ("unique_warranty_configuration", "UNIQUE(name, product_id)", "Warranty configuration already exists"),
        ("valid_percentage", "CHECK(percentage >= 0)", "Percentage must be positive"),
        ("valid_duration", "CHECK(duration > 0)", "Warranty duration must be greater than zero")
    ]
    
    name = fields.Char(string="Name", help="Warranty Name")
    product_id = fields.Many2one(comodel_name="product.template", domain=[("type", "=", "service")], required=True, ondelete="cascade")
    percentage = fields.Float(string="Percentage", required=True, help="Applies percentage cost of product to warranty")
    duration = fields.Integer(string="Duration (Years)", required=True, help="Warranty duration in years")
