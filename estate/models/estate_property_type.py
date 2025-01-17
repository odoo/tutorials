from odoo import api,fields,models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Types"
    _order= "name asc"

    name = fields.Char('Property Type', required=True)
    number = fields.Integer('Numbers')
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer('Sequence', default=1)
    offer_ids = fields.One2many('estate.property.offer','property_type_id',string='Offers')
    offer_count=fields.Integer(compute='_calculate_offers')


    _sql_constraints = [
        ('uniq_name', 'unique(name)' ,'Property Type Name should be unique'),
    ]
    

    @api.depends('offer_ids')
    def _calculate_offers(self):
     for record in self:
         record.offer_count = len(record.offer_ids)
