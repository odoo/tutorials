from odoo import api, fields, models


class PropertyType(models.Model):
    _name = "property.type"
    _description = "Property Type"
    _order = "name"

    name = fields.Char(required=True)
    offer_count = fields.Integer(compute="_compute_offer_count", string="Offer Count")
    sequence = fields.Integer(
        "Sequence", default=1, help="Used to manually order types based on sales."
    )

    # One2many relationship with property model
    property_ids = fields.One2many(
        string="Properties",
        comodel_name="estate.property",
        inverse_name="property_type_id",
    )
    offer_ids = fields.One2many(
        string="Offers",
        comodel_name="property.offers",
        inverse_name="property_type_id",
    )

    # sql constraints for unique property type name
    _sql_constraints = [
        ("unique_property_type", "unique(name)", "This property type already exists!")
    ]

    # compute method to count offers
    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
        return True
