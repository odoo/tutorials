from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order="sequence"


    name = fields.Char('Property Type', required=True)
    property_ids = fields.One2many('estate.property','property_type_id')
    sequence = fields.Integer('Sequence')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id',string="Offer Id")
    offer_count = fields.Integer("Offers" , compute='_compute_offer_count')
   
    _sql_constraints = [
    ('estate_property_type_name_unique', 'UNIQUE(name)', 'The property type must be unique.')]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
            
    
         




