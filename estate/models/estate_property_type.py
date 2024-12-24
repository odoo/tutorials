from odoo import api, models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name asc"

    name = fields.Char(required=True, string="Name")
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    sequence = fields.Integer(string="Sequence")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offer")
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")
    
    _sql_constraints = [
        ('check_expected_price', 'UNIQUE (name)', 'A property type name must be unique'),
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
