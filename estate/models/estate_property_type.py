from odoo import fields, models, api 

class EstatePropertyType(models.Model): 
    _name = "estate.property.type"
    _description = "Type of a Property"
    _order = "sequence, name"
    _sql_constraints = [("name_uniq", "UNIQUE(name)", "Property type name must be unique")]
    
    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    sequence = fields.Integer(string="Sequence", default=10) 
    offer_count = fields.Integer(string="Number of Offers", compute="_compute_offer_count")
    
    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self: 
            record.offer_count = len(record.offer_ids)