from odoo import api, fields, models


class estatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "the type of the property ..."
    _order = "sequence, name"
    _sql_constraints = [
        ('check_tag', 'UNIQUE(name)',
         'A property type name must be unique'),
    ]

    name = fields.Char("Name")
    property_ids = fields.One2many("estate.property", "type_id", string="Properties")
    sequence = fields.Integer("Secuence", default=1)
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="offers")
    offer_count = fields.Integer(string="Offers Count", compute="_compute_offers")

    @api.depends("offer_ids")
    def _compute_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
