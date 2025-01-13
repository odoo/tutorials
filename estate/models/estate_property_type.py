
from odoo import models,fields,api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Types"
    _order= "name asc"

    name = fields.Char('Property Type', required=True)
    number = fields.Integer('Numbers')
    property_ids = fields.One2many("estate.property", "estate_id")
    sequence = fields.Integer('Sequence', default=1, help="Used to order property types based on sequence.")
    offer_ids = fields.One2many(
        comodel_name='estate.property.offer',  
        inverse_name='property_type_id',  
        string='Offers' , 
    )
    offer_count=fields.Integer(compute='_calculate_offers')



    _sql_constraints = [
        ('uniq_name', 'unique(name)' ,'Property Type Name should be unique'),
    ]
    

    @api.depends('offer_ids')
    def _calculate_offers(self):
     for record in self:
         record.offer_count = len(record.offer_ids)





    