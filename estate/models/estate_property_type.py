from odoo import api, fields, models


class EstatePropertyType(models.Model):
    """Model representing types of real estate properties.

    This model defines categories for properties, such as 'Apartment', 'House', etc.,
    and tracks associated properties and offers. It includes a computed field for
    offer count.
    """

    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(string="Property Type", required=True)
    description = fields.Text(string="Description")
    sequence = fields.Integer(string="Sequence")
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )
    offer_ids = fields.One2many("estate.property", "property_type_id", string="Offers")
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")

    _sql_constraints = [
        ("unique_type_name", "UNIQUE(name)", "Property type name must be unique."),
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        """Compute the number of offers associated with this property type.

        Updates the `offer_count` field with the count of records in `offer_ids`.
        """
        for record in self:
            record.offer_count = len(record.offer_ids)
