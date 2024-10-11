from odoo import fields, models,api # type: ignore
from datetime import datetime, timedelta
from odoo.exceptions import UserError # type: ignore


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Model"

    
    # fields
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, string="Available From", 
                                    default=lambda self: datetime.today() + timedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades =  fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Direction',
        selection=[('north', 'North'), ('south', 'South'),('east', 'East'),('west', 'West')],
        help="Direction selection from North,South,East,West")
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        string='State',
        copy=False,
        default='new',
        selection=[('new', 'New'), ('offer received', 'Offer Recieved'),('offer accepted', 'Offer Accepted'),('sold', 'Sold'),('canceled', 'Canceled')],
        help="Direction selection from North,South,East,West")
    property_type_id = fields.Many2one(
        'estate.property.type', 
        string='Property Type',
    )
    salesperson = fields.Many2one(
        'res.users',
        string = 'Salesman',
        default=lambda self: self.env.user
    )
    buyer = fields.Many2one(
        'res.partner',
        string = 'Buyer',
        copy= False
    )
    tag_ids = fields.Many2many(
        'estate.property.tags',
        string = "Tags"
    )
    offer_ids = fields.One2many(
        'estate.property.offers',
        "property_id",
        # string= "Offers"
    )
    total_area = fields.Float(compute = "_compute_area", string = "Total Area (sqm)")

    best_price = fields.Float(compute = "_compute_best_price", store=True)

    # Functions
    @api.depends('living_area', 'garden_area')
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
            

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            # max_price = 0
            # for offer in record.offer_ids:
            #     max_price = offer.price if offer.price > max_price else max_price
            # record.best_price = max_price
            # by mapped method
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0
    
    @api.onchange('garden_area', 'garden_orientation', 'garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False
    
    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("You cannot mark a canceled property as sold.")
            record.state == 'sold'

            