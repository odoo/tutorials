from odoo import fields, models

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(
        "Property Tag", required = True,
        help = "This is a Many2many Field that define tags which can be associated to a property."
    )

    _sql_constraints = [('tag_unique', 'unique(name)', 'Property Tag should be unique.')]
