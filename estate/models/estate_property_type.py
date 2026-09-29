from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer("Sequence", default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(compute="_compute_offer_count")
    _order = "sequence, name"

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _unique_import_id = models.Constraint(
        'unique (name)',
        "This name is already taken",
    )
