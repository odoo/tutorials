from odoo import api, fields, models


class EstateTypeModel(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type Model"
    _order = "sequence, name desc"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer(
        "Sequence", default=1, help="Used to change the sequence of Property Types"
    )
    offer_ids = fields.One2many(
        "estate.property.offer", inverse_name="property_type_id"
    )
    offer_count = fields.Integer(
        default=0, readonly=True, compute="_compute_offers_by_type"
    )

    _sql_constraints = [
        (
            "check_property_type_name",
            "UNIQUE(name)",
            "Property Type Name must be unique",
        )
    ]

    @api.depends("offer_ids")
    def _compute_offers_by_type(self):
        self.offer_count = len(self.offer_ids)
