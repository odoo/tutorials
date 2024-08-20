from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "This model stores the estate property types and general informations about them"
    _order = "name"
    _sql_constraints = [
        ('unique_type', 'UNIQUE (name)', 'all types must have a unique name')
    ]

    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    property_ids = fields.One2many("estate.property", "property_type_id")

    name = fields.Char(string="Type", required=True)
    description = fields.Text(string="Description")
    offer_count = fields.Integer(string="Offers", compute="_compute_offer_count")
    sequence = fields.Integer('Sequence', default=1)

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for estate_type in self:
            count = 0
            for offer in estate_type.offer_ids:
                if offer.property_id.state == 'offer_received':
                    count += 1
            estate_type.offer_count = count
