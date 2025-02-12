from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tags'
    _description = "Property tags such as cozy, renovated, etc."
    _order = 'name'

    name = fields.Char(
        string="Tag Name",
        required=True,
        help="The name of the property tag (e.g., Cozy, Renovated)"
    )

    color = fields.Integer(
        string="Color",
        help="Color index used for displaying the tag"
    )

    _sql_constraints = [
        (
            'unique_property_tag_name',
            'UNIQUE(name)',
            "The name must be unique"
        )
    ]
