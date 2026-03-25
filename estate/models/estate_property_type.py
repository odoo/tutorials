from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Estate property types"
    _order = "sequence, name"

    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

    name = fields.Char(required=True)
    _check_name = models.Constraint(
        'UNIQUE(name)',
        "The name of property type must be unique.",
    )

    property_ids = fields.One2many('estate.property', 'property_type_id')

    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
        return True
