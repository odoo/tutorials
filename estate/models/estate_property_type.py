from odoo import api,fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type Model"
    _order = "sequence, name"
    _sql_constraints = [('name_unique','unique(name)',"this property type is already exists!")]
    
    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1,help="Used to order stages.")
    offer_count = fields.Integer(compute='_compute_offers')
    property_ids = fields.One2many('estate.property','property_type_id',string="Properties")
    offer_ids = fields.One2many('estate.property.offer', "property_type_id",string='Offers')
    
    @api.depends("offer_ids")
    def _compute_offers(self):
        for record in self:
            record.offer_count=len(record.offer_ids)
