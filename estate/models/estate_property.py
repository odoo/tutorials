from datetime import date, timedelta
from odoo import api, fields, models  # type: ignore

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Application Ayve"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: (date.today() + timedelta(days=90)).strftime('%Y-%m-%d'), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Integer(compute="_total_area", store=True)
    best_price=fields.Integer(compute="_compute_best_price", store=True)
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string='Garden Orientation',
        help='Select One Orientation'
    )
    active = fields.Boolean(default=True)
    
    state = fields.Selection(
    [
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ],
        string='State',
        default='new',
        copy=False,
        help='Select the current status of the property'
    )

    # ONE property can have only ONE property type
    # But ONE property type can be assigned to MANY properties
    property_type_id=fields.Many2one(
        "estate.property.type",
        string="Property Type"
    )

    # ONE property can have only ONE buyer and seller
    # But ONE  buyer/seller can sell/buy MANY properties
    seller_id=fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user
    )

    buyer_id=fields.Many2one(
        "res.partner",
        string="Buyer"
    )

    # MANY tags can  se assigned to multiple properties and vice versa
    tag_ids=fields.Many2many(
        "estate.property.tag",
        string="Property Tags"
    )

    # A property can have MANY offers 
    # But ONE offer can only be applied to ONE property
    # For Every One2many there should be a Many2one but not vice versa
    offer_ids=fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers"
    )

    @api.depends("living_area","garden_area")
    def _total_area(self):
        for line in self:
            line.total_area = line.living_area + line.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.mapped("offer_ids.price"), default=0)

    #Onchange Methods
    '''In many cases, both computed fields and onchanges may be used to achieve the
    same result. Always prefer computed fields since they are also triggered outside
    of the context of a form view. Never ever use an onchange to add business logic 
    to your model. This is a very bad idea since onchanges are not automatically 
    triggered when creating a record programmatically; they are only triggered in the form view.'''

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None
    
    # Actions for button
    def sold_button(self):
        for record in self:
            record.state = "sold"
        return True
    
    def cancel_button(self):
        for record in self:
            record.state = "canceled"
        return True
        