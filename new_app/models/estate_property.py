from odoo import fields, models, api
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Table"

    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Description", default='bla bla bla')
    postcode = fields.Char(string="Postcode", default='456010')
    # date_availability = fields.Date()
    date_availability = fields.Date(string="Availability Date", readonly=False,
                                    copy=False, default=fields.Datetime.today() + relativedelta(days=60))
    expected_price = fields.Float(
        string="Expected Price", default='1500000.00', required=True)
    selling_price = fields.Float(string="Selling Price", default='1500000.00')
    living_area = fields.Integer(string="Living area (sqm)", default='15465')
    facades = fields.Integer(string="Facades", default='4')
    bedroom = fields.Integer(string="Bedrooms", default='2')
    garage = fields.Boolean(string="Garage", default=True)
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ], default='north', required=True)
    

    # Reserved field with default value True
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ], copy=False, default='new', required=True)               # Reserved field with default state as New
    
    
    # Chapter 7
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type")
   
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,  # Default is the current user
        required=True
    )

    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False  # Buyer should not be copied
    )

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers"
    )



    # Chapter-8
    # exercise-1
    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_total_area")
 
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    
    
    # exercise-2, best offer 
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.mapped("offer_ids.price"))
            else:
                record.best_price = 0.0

    
    # exercise-3 (onchange function)
    @api.onchange("garden")
    def _onchange_garden(self):
        # automatically set or clear garden realted fields when garden is toggled
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = False
                # clear the selection as I have write False
            

