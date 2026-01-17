from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer()
    
    _check_tag_name = models.Constraint(
        "UNIQUE(name)", "The property tag name must be unique"
    )
