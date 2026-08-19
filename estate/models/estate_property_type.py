from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'sequence, name'

    name = fields.Char('Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=1, help="Used for ordering purposes")
    property_id = fields.One2many('estate.property', 'property_type_id', string='Property')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    # Compute Field
    offer_count = fields.Integer(string='Offer Count', compute='_compute_offer_count')

    _name_uniq = models.Constraint(
        'unique (name)',
        'There is already a Property Type with this name!.',
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

