from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"
    _check_tag_name = models.Constraint(
        "UNIQUE(name)", "A property tag name should be unique."
    )

    name = fields.Char(required=True)
    color = fields.Integer()
