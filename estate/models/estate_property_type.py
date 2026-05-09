from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'estate property types'
    _order = 'name'

    _name_uniq = models.Constraint(
        'unique (name)',
        'Name already Exists',
    )

    name = fields.Char(required=True)
    price = fields.Integer()
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer(default=1)
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends('name', 'price')
    @api.depends_context('formatted_display_name')
    def _compute_display_name(self):
        for types in self:
            if types.env.context.get('formatted_display_name'):
                price_prefix = f'\t--( rs.{types.price} )--'
                types.display_name = f'{types.name} {price_prefix.strip()}'
            else:
                types.display_name = f'{types.name} ( rs.{types.price} )'

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)
