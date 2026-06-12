from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence,name"

    name = fields.Char()
    sequence = fields.Integer(
        string="Sequence",
        default=1,
        help="Used to order property types manually."
    )

    property_ids = fields.One2many(
        "estate.property",
        "property_type_id",
        string="Properties"
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_type_id",
        string="Offers"
    )

    offer_count = fields.Integer(
        string="Offers Count",
        compute="_compute_offer_count"
    )

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'Property type name must be unique!',
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
