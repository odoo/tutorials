from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type Model"
    _order = "sequence"

    name = fields.Char(
        string="Property Type",
        required=True,
    )
    property_ids = fields.One2many(
        "estate.property",
        "property_type_id",
    )
    sequence = fields.Integer(
        'Sequence',
        default=1,
        help="Used to order stages. Lower is better.",
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_type_id",
    )
    offer_count = fields.Integer(compute="_compute_total_offers")

    _check_name_unique = models.Constraint("UNIQUE(name)", "Property type must be unique.")

    def _compute_total_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
