from odoo import api, exceptions, fields, models
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_compare, float_is_zero

class RealEstate(models.Model):
    _name = "real.estate.property"
    _description = 'Real State properties'
    _order = "id desc"

    name = fields.Char(string = 'Title', required = True)
    image = fields.Binary("")
    description = fields.Text(string = 'Description')
    postcode = fields.Char(string = 'Postcode')
    date_availability = fields.Date(string = 'Available From', copy = False, default = fields.Datetime.now() + relativedelta(months=3))
    expected_price = fields.Float(string = 'Expected Price', required = True)
    selling_price = fields.Float(string = 'Selling Price', readonly = True, copy = False)
    bedrooms = fields.Integer(string = 'Bedrooms', default = 2)
    living_area = fields.Integer(string = 'Living Area (sqm)')
    facades = fields.Integer(string = 'Facades')
    garage = fields.Boolean(string = 'Garage', )
    garden = fields.Boolean(string = 'Garden')
    garden_area = fields.Integer(string = 'Garden Area (sqm)')
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string = 'Garden Orientation'
    )
    status = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        default = 'new',
        string = 'Status',
        copy = False,
    )
    active = fields.Boolean(string = "Active", default = True)
    property_type_id = fields.Many2one('real.estate.property.category', string = "Property Type")
    partner_id = fields.Many2one("res.partner", string = "Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string = "Salesman", default = lambda self: self.env.user)
    tag_ids = fields.Many2many('real.estate.property.tag', string = "Tag")
    offer_ids = fields.One2many('real.estate.property.offer', 'property_id', string = 'Offer', copy = False)
    total_area = fields.Float(compute = "_compute_total_area", string = "Total Area (sqm)", readonly = True)
    best_price = fields.Float(compute = "_compute_best_price", string = "Best Offer", readonly = True, default = 0, copy = False)

    #sql constraints to check that expected and selling price is not a negative number
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'A property expected price must be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'A property expected price must be positive')
    ]

    #depends method to calculate total area based on garden area and living area
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    #depends method to calculate best offer among all other offers
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    #onchange method to give default garden area and garden orientation if garden is selected
    @api.onchange("garden")
    def _onchange_garden_details(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = ''
            self.garden_orientation = ''

    #method to sold property 
    def action_property_sold(self):
        if self.status == 'cancelled':
            raise exceptions.UserError("Cancelled properties cannot be sold.")
        elif not self.offer_ids:
            raise exceptions.UserError("There is no offer for this property.")           
        else:
            for record in self.offer_ids:
                if record.status == 'accepted':
                    self.status = 'sold'
                    break
            if self.status != 'sold':    
                raise exceptions.UserError("Accept the offer.")
        return
        
    #method to cancel property
    def action_property_cancel(self):
        if self.status == 'sold':
            raise exceptions.UserError("Sold properties cannot be cancelled.")
        else:
            self.status = 'cancelled'
            is_accepted_offers = self.offer_ids.filtered(lambda x: x.status == 'accepted')
            if is_accepted_offers:
                is_accepted_offers.status = 'refused'
            else:
                for offer in self.offer_ids:
                    offer.status = 'refused'
        return

    #Python constraint to check that selling price is 90% of expected
    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, 2):
                if(float_compare((record.expected_price * 0.9), (record.selling_price), 2) == 1):
                    raise exceptions.ValidationError("The selling price cannot be lower than 90% of the expected price.")

    #Overriding delete method to prevent deletion of some property
    @api.ondelete(at_uninstall=False)
    def _unlink_if_property_cancel_new(self):
        if any(record.status in ('offer_received', 'offer_accepted', 'sold') for record in self):
            raise exceptions.UserError("Only new and cancelled properties can be deleted.")
