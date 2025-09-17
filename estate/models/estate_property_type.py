from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Property Type"
    _order = 'sequence, name'
    
    _unique_name = models.Constraint(
        'unique(name)',
        "Property type name must be unique.",
    )

    name = fields.Char("Property Type", required=True)
    
    property_ids = fields.One2many(
        comodel_name='estate.property',
        inverse_name='property_type_id',
        string="Properties",
    )
    offer_ids = fields.One2many(
        comodel_name='estate.property.offer',
        inverse_name='property_type_id',
        string="Offers",
    )
    offer_count = fields.Integer(string="Offer Count", compute='_compute_offer_count')

    sequence =fields.Integer("Sequence", default=1, help="Used to order property types.")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = len(property_type.offer_ids)
