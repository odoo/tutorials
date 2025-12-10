from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _check_tag_name = models.Constraint(
        "UNIQUE(name)", "Property tag should be unique."
    )
    name = fields.Char(required=True)
