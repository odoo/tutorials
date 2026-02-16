from odoo import api, fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence"

    name = fields.Char(string="Property Type", required=True)
    estate_property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    sequence = fields.Integer("Sequence", default=1)
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer("# Offers", compute="_compute_offer_count")

    _check_type_uniqueness = models.Constraint(
        'unique(name)',
        'This type is already used, please use it or add a new type',
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
