from odoo import models, fields, api


class estatepropertytype(models.Model):
    _name = "estate.property.type"
    _description = "adding property type"
    _order = "name"

    name = fields.Char("Property Types", required=True)
    _sql_constraints = [
        (
            "property_type_uniq",
            "unique(name)",
            "A property_type with the same name already exists in this estate.",
        )
    ]
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer", inverse_name="property_type_id"
    )
    offer_count = fields.Integer(compute="_num_of_offers", string="Offer Count")
    sequence = fields.Integer(
        "Sequence", default=1, help="Used to order propertypes manually"
    )

    @api.depends("offer_ids")
    def _num_of_offers(self):
        for record in self:

            record.offer_count = len(record.offer_ids)
