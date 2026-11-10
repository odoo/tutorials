from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    name = fields.Char(required=True)
    _name_unique = models.Constraint("unique(name)", "Type must be unique")
    property_ids = fields.One2many("estate.property", "type_id", string="Properties")
    _order = "sequence, name"
    sequence = fields.Integer(
        "Sequence", default=1, help="Used to order property types"
    )
    offer_ids = fields.One2many(
        "estate.property.offer", "property_type_id", string="Offers"
    )
    offer_count = fields.Integer("Offer Count", compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
