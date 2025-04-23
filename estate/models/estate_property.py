from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate model"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available From", copy=False, default=fields.Datetime.add(fields.Datetime.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string='Garden orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Allows to know where the sun is about the home")
    active = fields.Boolean(default=False)
    state = fields.Selection(string="Status",
                             required=True,
                             copy=False,
                             default="new",
                             selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')])
    
    # Many2One relationships
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    salesperson_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)

    # Many2Many relationships
    tag_ids = fields.Many2many('estate.property.tag')
    
    # One2Many relionships
    offer_ids = fields.One2many('estate.property.offer', 'property_id')