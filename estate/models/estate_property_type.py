from odoo import api, fields, models


class Type(models.Model):
    _name = "estate.property.type"
    _description = "Property type"
    _order = "sequence"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1, help="Used to order stages. Lower is better.")
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _name_uniq = models.Constraint('unique(name)', 'This property type allready exist')

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
