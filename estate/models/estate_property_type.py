from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "A property type is, for example, a house or an apartment. It is a standard business need to categorize properties according to their type, especially to refine filtering."
    _order = "name asc"

    name = fields.Char('Property type', required=True)
    _unique_name = models.Constraint(
        'unique (name)',
        'A property type name must be unique.'
    )

    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    sequence = fields.Integer('Sequence', default=1, help="Used to order types. Lower is better.")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer('Offer count', compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
