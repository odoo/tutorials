from odoo import api,fields, models, exceptions

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description =  "Property Types"
    _order  = "sequence, name"

    name = fields.Char(string='Name', required=True)
    property_ids = fields.One2many('estate.property','property_type_id')
    sequence = fields.Integer(string='Sequence', default=1)
    offer_ids = fields.One2many('estate.property.offer','property_id', string='Offers')
    offer_count = fields.Integer(string="Offers", compute='_compute_offers')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Type name already exists!"),
    ]

    @api.depends('offer_ids')
    def _compute_offers(self):
        for record in self:
            count = 0
            for property in record.property_ids:
                count += len(property.offer_ids)
            record.offer_count = count
