from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Types"
    _name_unique = models.Constraint(
        "UNIQUE(name)", "Property type needs to be unique.",
    )
    _order = "sequence,name"

    name = fields.Char(string="Property Type", required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order Property. Lower number more priority.")
    property_ids = fields.One2many('estate.property', 'property_type_id', string='property')

    offer_ids = fields.One2many(
        string='offer',
        comodel_name='estate.property.offer',
        inverse_name='property_type_id',
    )
    offer_count = fields.Integer(compute="_compute_offers")

    @api.depends('offer_ids')
    def _compute_offers(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)
