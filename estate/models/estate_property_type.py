from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"
    _order = "sequence, name asc"

    name = fields.Char('Property Type', required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    house_ids = fields.One2many(
        string='Properties',
        comodel_name='estate.property',
        inverse_name='property_type_id'
    )
    offer_ids = fields.One2many(
        string='Offers',
        comodel_name='estate.property.offer',
        inverse_name='property_type_id'
    )
    offer_count = fields.Integer(string='Offer quantity', compute='_compute_total_offers')

    _check_duplicates = models.Constraint(
        'UNIQUE(name)',
        'This type already exist',
    )

    @api.depends('offer_ids')
    def _compute_total_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
