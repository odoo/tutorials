from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag for Estate Property"
    _order = "name"
    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.estate.property", "tags_ids")
    color = fields.Integer()

    ## SQL Constraints Section ##
    _check_name = models.Constraint(
        'UNIQUE(name)',
        'A tag should be unique'
    )