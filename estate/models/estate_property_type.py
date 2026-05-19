from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "type of the estate property"
    _order = "name"

    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_type_id",
        string="Offers",
    )
    offer_count = fields.Integer(compute="_compute_offer_count")
    active = fields.Boolean(default=True)
    name = fields.Char(required=True)
    sequence = fields.Integer(string="Sequence", default=1, help="Used for ordering")
    property_ids = fields.One2many(
        "estate.property",
        "property_type_id",
        string="Properties",
    )

    _name_uniq = models.Constraint(
        "unique (name)",
        "Each property type name must be unique.",
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        self.offer_count = len(property.offer_ids)
