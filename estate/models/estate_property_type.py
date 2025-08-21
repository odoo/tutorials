from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "A type with same name is already exists."),
    ]
    _order = "sequence,name"

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        comodel_name="estate.property",
        inverse_name="property_type_id",
        string="Properties",
    )
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    sequence = fields.Integer(
        "Sequence", default=1, help="Used to order types. Lower is better."
    )

    offer_count = fields.Integer("Offers", compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
