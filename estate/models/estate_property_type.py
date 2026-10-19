from odoo import api, fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "this is used to define the types"
    _order = "sequence, name"

    name = fields.Char(required=True, string="Type")
    property_id = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer("Sequence")
    offer_ids = fields.One2many("estate.property.offers", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offers")

    _check_name = models.Constraint(
        "unique(name)", "The name of the property type must be unique"
    )

    @api.depends("offer_ids")
    def _compute_offers(self):
        for rec in self:
            count = 0
            for offer in rec.offer_ids:
                if rec.name == offer.property_type_id.name:
                    count += 1
            rec.offer_count = count
