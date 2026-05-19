from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property's tag"
     
    # Order attributes
    _order = "name"

    name = fields.Char(required=True,)
    color = fields.Integer(string="Color",)

    # -------------------------------------------------------------------------
    # CONSTRAINTS
    # -------------------------------------------------------------------------
    _unique_tag_name = models.Constraint(
        'UNIQUE(name)', 
        'A property tag name must be unique.',
    )
