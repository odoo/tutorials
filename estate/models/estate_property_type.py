from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Types"
    _order = "name"

    name = fields.Char(string="Name", required=True)
    _name_unique = models.Constraint(
        'unique(name)',
        '2 property type names cannot be same ',
    )
    property_id = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer(string="Sequence")
    color = fields.Integer()
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offer Ids")
    offer_count = fields.Integer(string="offer count", compute="_compute_offer_count")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
