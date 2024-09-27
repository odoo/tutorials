from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = "estate.property.type"
    _description = "EstatePropertyType"
    _order = "name"

    # created the fields for the estate.property.type model
    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer(
        "Sequence", default=1, help="Used to order stages. Lower is better."
    )
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count", string="Offer Count")

    # created the compute function to compute the offer count
    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    # created the sql constraints for unique property type
    _sql_constraints = [
        ("unique_name", "unique(name)", "A property type name must be unique.")
    ]
