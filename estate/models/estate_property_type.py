from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "name"

    # -------------------------------------------------------------------------
    # SQL QUERIES
    # -------------------------------------------------------------------------

    _sql_constraints = [
        ('uniq_name', 'unique(name)', 'The name of the type must be unique.')
    ]

    name = fields.Char(
        string="Name",
        help="The name of the property type.",
        required=True
    )
    property_ids = fields.One2many(
        string="Properties",
        help="The properties of this type.",
        comodel_name="estate.property",
        inverse_name="property_type_id"
    )
    sequence = fields.Integer(
        string="Sequence",
        help="The sequence of the property type.",
        default=1
    )
    offer_ids = fields.One2many(
        string="Offers",
        help="The offers for properties of this type.",
        comodel_name="estate.property.offer",
        inverse_name="property_type_id"
    )
    offer_count = fields.Integer(
        string="Offer Count",
        help="The number of offers for properties of this type.",
        compute="_compute_offer_count"
    )

    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
