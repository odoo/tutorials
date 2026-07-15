from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"


    name = fields.Char(required=True)
    property_ids = fields.One2many(
        "estate.property",
        # link each property to a single property type
        "property_type_id",
        string="Properties",
    )
    sequence = fields.Integer(default=1)
    # STAT BUTTON
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_type_id",
        string="Offers",
    )
    offer_count = fields.Integer(
        compute="_compute_offer_count"
    )

    # SQL Constraints
    # Property type name must be unique
    _unique_property_type = models.Constraint(
        'UNIQUE(name)',
        'The property type must be unique',
    )

    # STAT BUTTON
    # Whenver offer_ids changes recompute offer count
    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for property_type in self:
            # offer_ids is a recordset 
            # len returns number of records in the recordset
            property_type.offer_count = len(property_type.offer_ids)