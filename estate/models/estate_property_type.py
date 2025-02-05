from odoo import models, fields


class EstatePropertyType(models.Model):
    _name="estate.property.type"
    _description="Real Estate Property Type"
    
    name = fields.Char(string="Name", required=True, help="Property Type")
    active = fields.Boolean(default=True)
