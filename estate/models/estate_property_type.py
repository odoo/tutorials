from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Estate Property Type"
    _order = "name"

    sequence = fields.Integer('Sequence', default=1,
                              help="Used to order Property Type")
    name = fields.Char("Property Type", required=True)
    ofr_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer')
    property_ids = fields.One2many(
        'estate.property', "property_type_id", required=True
    )

    # SQL CONSTRAINT
    _property_type_uniq = models.Constraint(
        'UNIQUE(name)', "Property Type already exist in database"
    )

    # DEPEND DECORATOR
    @api.depends('ofr_ids')
    def _compute_offer(self):
        for record in self:
            record.offer_count = len(record.ofr_ids)
