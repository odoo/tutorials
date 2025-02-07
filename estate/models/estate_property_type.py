from odoo import models, fields

class EstatePropertyType(models.Model):
    _name="estate.property.type"
    _description="Real Estate Property Type"
    _order = "Sequence" 

    name=fields.Char(string="Name" , required=True)
    expected_price = fields.Float(string="Expected Price", required=True)
    state = fields.Selection([
        ('new', 'New'),('offer_received', 'Offer Received'),('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),('cancelled', 'Cancelled'),],
        string="State", default='new')


    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 
         'Property type names must be unique.')
    ]
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    Sequence = fields.Integer('Sequence', default=10)
    
