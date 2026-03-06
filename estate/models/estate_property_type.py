from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Types"
    _order = "sequence,name"

    name = fields.Char(string="Property Type", required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order Property. Lower number more priority.")
    property_ids = fields.One2many('estate.property', 'property_type_id', string='property')

    # chaloooooooooo
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

    def button_recompute_offers(self):
        self._compute_offers()
        return True
