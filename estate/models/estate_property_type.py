from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence,name"

    name = fields.Char(required=True)
    sequence = fields.Integer()
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_type_id",
        string="Offers",
    )

    offer_count = fields.Integer(
        string="Offer Count",
        compute="_compute_offer_count",
    )

    _sql_constraints = [
        ("unique_name_field", "UNIQUE(name)", "The name must be unique."),
    ]

    # compute method : offer count
    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)
