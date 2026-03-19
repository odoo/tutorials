from odoo import models, fields ,api 


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'sequence, name'


    name = fields.Char(required = True)

    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

    property_ids = fields.One2many(comodel_name='estate.property', inverse_name='property_type_id', string="Properties")

    offer_ids = fields.One2many(comodel_name='estate.property.offer' , inverse_name='property_type_id' , string="Offers" )

    _check_unique_tag = models.Constraint(
        'UNIQUE(name)', "A property type name must be unique!"
    )


    offer_count = fields.Integer(compute="_compute_offer_count", string="Offer Count")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
