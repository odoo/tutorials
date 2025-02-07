from odoo import fields, models

class estate_Property(models.Model):
    _name = "estate_model"  
    _description = "This is the description for esatet properties model:"

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    postcode = fields.Integer()
    date_availability = fields.Date(copy=False,default=fields.Date.today())
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection = [('north', 'North'), ('east', 'East'), ('south', 'South'),('west', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection(copy=False, required=True, default='new',
        selection = [('new', 'New'), ('offerr_received', 'Offer_Received'), 
        ('offer_accepted', 'Offer_accepted'), ('sold', 'Sold')])
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)