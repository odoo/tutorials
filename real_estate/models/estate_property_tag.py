from odoo import fields, models


class EstatePropertyTag(models.Model):
    """Model representing property tags (e.g., Cozy, Renovated, Luxury).
    
    Tags help categorize properties based on their features.
    """
    _name = 'estate.property.tags'
    _description = "Property tags such as cozy, renovated, etc."
    _order = 'name'  # Sort tags alphabetically by name

    name = fields.Char(
        string="Tag Name",
        required=True,
        help="The name of the property tag (e.g., Cozy, Renovated, Luxury)"
    )
    color = fields.Integer(
        string="Color",
        help="Color index used for displaying the tag in the UI"
    )
    # Enforce uniqueness constraint on the tag name
    _sql_constraints = [
        (
            'unique_property_tag_name',
            'UNIQUE(name)',
            "The tag name must be unique"
        )
    ]
