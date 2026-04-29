from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name"

    name = fields.Char(required=True, string="Property Type Name")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

    property_ids = fields.One2many("estate.property", "estate_property_type_id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")

    offer_count = fields.Integer(compute="_compute_offer_count", string="Offer Count")

    _name_uniq = models.Constraint(
        "unique (name)",
        "Property Type name must be unique",
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

