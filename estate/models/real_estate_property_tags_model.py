from odoo import fields,models

class PropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Real estate Tags"
    _sql_constraints = [
        ("estate_property_tag_constraint","UNIQUE(name)","Each tag should be unique" ),
    ]
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()
    