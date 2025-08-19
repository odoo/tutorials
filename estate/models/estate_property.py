from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

  

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availaility = fields.Date(default=(fields.Date.add(fields.Date.today(), days=90)), copy=False)
    
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly = True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string = 'Type',
        selection=[('North','north'),('South','south'),('East','east'),('West','west')],
        help="Type is used to know the direction of the Garden ")
    active = fields.Boolean(default = True)
    state = fields.Selection([   ('new', 'New'),
    ('offer_received', 'Offer Received'),
    ('offer_accepted', 'Offer Accepted'),
    ('sold', 'Sold'),
    ('cancelled', 'Cancelled'),],required=True, copy=False, default='new')
    property_type = fields.Many2one("estate.property.type", string="Property Type")
    salesman = fields.Many2one("res.users", default = lambda self: self.env.user)
    buyer = fields.Many2one("res.partner", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offers_ids = fields.One2many("estate.property.offers", "property_id")





