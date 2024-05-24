from odoo import fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "estate property"
    
    # simple fields
    name = fields.Char()
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date("Available From", copy=False, default=fields.Datetime.add(fields.Datetime.now(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)", default=1)
    facades = fields.Integer(default=1)
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area (sqm)")
    active = fields.Boolean()

    garden_orientation = fields.Selection(
        selection=[('north', "North"), ('south', "South"), ('east', "East"), ('west', "West")],
        help="orientation of the garden relative to the property",
        )
    state = fields.Selection(
        string="Status",
        selection=[('new', "New"),
                   ('offer_received', "Offer Received"),
                   ('offer_accepted', "Offer Accepted"),
                   ('sold', "Sold"),
                   ('canceled', "Canceled"),
                   ],
        required=True,
        default='new',
        copy=False,
        )
    
    # relational fields
    property_type_id = fields.Many2one('estate.property.type', string="Type")
    buyer_id = fields.Many2one('res.partner', copy=False)
    salesperson_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many('estate.property.tag', string="Tag")
    offer_ids = fields.One2many('estate.property.offer', "property_id")
    