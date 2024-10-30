from odoo import fields, models


class EstatePropertyType(models.Model):

    _name = "estate.property.type"
    _description = "Estate Property Type Model"
    _order = "sequence,name"
    _sql_constraints = [
        ('check_unique_name', 'UNIQUE(name)',
         'This property type name already exists'),
    ]
    name = fields.Char(required=True)
    property_ids = fields.One2many(comodel_name="estate.property", inverse_name="property_type_id", string="Property")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many('estate.property.offers', 'property_type_id', string='Offers')
    offer_count = fields.Integer(compute="_compute_number_of_offers")

    def _compute_number_of_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
