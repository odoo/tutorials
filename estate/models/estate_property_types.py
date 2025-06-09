from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer(
        string="Sequence",
        help="Used to order types. Lower is better.",
        default=1,
    )
    property_ids = fields.One2many(
        comodel_name="estate.property",
        string="Properties",
        inverse_name="property_type_id",
    )
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        string="Offers",
        inverse_name="property_type_id",
    )
    offer_count = fields.Integer(
        compute="_compute_offer_count",
    )

    _sql_constraints = [
        ("name_unique", "unique (name)", "Type name must be unique!"),
    ]

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
