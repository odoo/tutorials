from odoo import models, fields


class BuildingType(models.Model):
    _name = 'estate.building_type'
    _description = 'Building Type'
    _order = "sequence, name"

    name = fields.Char(required=True)
    building_ids = fields.One2many(
        "estate.buildings", "building_type_id", string="Buildings"
    )
    offer_ids = fields.One2many(
        "estate.offers", "property_type_id", string="Offers"
    )
    offers_count = fields.Integer(
        string="Offers Count",
        compute="_compute_offers_count",
    )

    _name_uniqueness_constraint = models.Constraint(
        "UNIQUE (name)", "Building type name must be UNIQUE."
    )

    sequence = fields.Integer(default=1, help="Gives the sequence order when displaying a list of building types.")

    def _compute_offers_count(self):
        for record in self:
            record.offers_count = self.env['estate.offers'].search_count([('property_type_id', '=', record.id)])
