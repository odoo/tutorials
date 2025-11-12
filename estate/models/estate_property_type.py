from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)
    property_ids = fields.One2many(comodel_name = "estate.property",  inverse_name="property_type_id" , string="Properties")
    _order = "name"
    offer_ids = fields.One2many("estate.property.offer" , "property_type_id" , string = "Offers")
    offer_count = fields.Integer(compute="_compute_offer_count" , string = "Offer Count") 
    sequence = fields.Integer()
    _sql_constraints = [
        ("check_name" , "UNIQUE(name)" , "The property type must be unique")
     ]
    
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
