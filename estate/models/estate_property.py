from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"
    
    
    active = fields.Boolean(default=True)
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Datetime(copy=False, default=fields.Datetime.add(fields.Datetime.now(), months=+3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        help="What is the orientation of the facade of the property"
    )
    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'), 
            ('offer-received', 'Offer received'), 
            ('offer-accepted', 'Offer accepted'), 
            ('sold', 'Sold'), 
            ('cancelled', 'Cancelled')
        ],
        required=True,
        copy=False,
        default='new'
    )

    property_type_id = fields.Many2one("estate.property.type", string="Type")
    user_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False) 
    property_tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
