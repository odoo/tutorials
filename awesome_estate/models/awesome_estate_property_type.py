from odoo import _, api, fields, models


class AwesomeEstatePropertyType(models.Model):
    _name = 'awesome.estate.property.type'
    _description = 'Real Estate Property Type'
    _order = 'sequence, name'

    name = fields.Char(required=True)
    sequence = fields.Integer(string="Sequence", default=10)
    property_ids = fields.One2many(
        'awesome.estate.property',
        'property_type_id',
        string="Properties",
    )
    offer_ids = fields.One2many(
        'awesome.estate.property.offer',
        'property_type_id',
        string="Offers",
    )
    offer_count = fields.Integer(
        string="Offer Count",
        compute='_compute_offer_count',
        store=True,
    )

    # -----------------------------------------------------------------------
    # SQL Constraints
    # -----------------------------------------------------------------------
    _check_type_name_unique = models.Constraint(
        'UNIQUE(name)',
        'The property type name must be unique.',
    )

    # -----------------------------------------------------------------------
    # Computed Fields
    # -----------------------------------------------------------------------
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = self.env['awesome.estate.property.offer'].search_count([
                ('property_type_id', '=', record.id),
            ])
