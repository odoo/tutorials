from odoo import fields, models

class estatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(string="Color",default = 0)

    #constraint
    _sql_constraints = [
        ("unique_property_tag_name", "UNIQUE(name)", "The property tag name must be unique."),
    ]