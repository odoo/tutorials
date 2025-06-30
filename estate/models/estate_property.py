from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc, name asc" 
    
    name = fields.Char("Title", required=True, default="Unknown")
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From",   default=lambda self: date.today() + relativedelta(months=3))
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Garden Orientation",
    )
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    active = fields.Boolean("Active", default=False)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type",
        string="Property Type",
        required=True,
    )
    property_tag_ids = fields.Many2many(
        comodel_name="estate.property.tag",
        string="Property Tags",
        help="Tags to categorize the property",
    )
    buyer_id = fields.Many2one('res.partner', string="Buyer")
    salesperson = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
        string="Offers",
        help="Offers made on the property",
    )
    total_area = fields.Integer(
        string="Total Area",
        compute="_compute_total_area",
        store=True, 
        help="Total area of the property, including living area and garden area",
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area 
    best_price = fields.Float(
        string="Best Price",
        compute="_compute_best_price",
        store=True,
        help="Best price from offers made on the property",
    )
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property in self :
            property.best_price = max(property.offer_ids.mapped('price'), default=0.0)

    @api.onchange('garden', 'garden_area')
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = False
        else:
            self.garden_area = 10
            self.garden_orientation = 'north'  

    def action_sold(self):
        if 'Canceled' in self.mapped('state'):
            raise UserError("Cannot mark as sold if there are canceled properties.")
        return self.write({'state': 'sold'})
    
    
    def action_cancel(self):
        if 'Sold' in self.mapped('state'):
            raise UserError("Cannot cancel a property that is already sold.")
        return self.write({'state': 'canceled'})
    
    


    
    # SQL Constraints
    _sql_constraints = [ 
        ('check_expected-price', 'CHECK(expected_price > 0','Expected price must be greater than 0.'),
        ('check_selling_price', 'CHECK(selling_price >= 0','Selling price must be greater than or equal to 0.'),
        ('check_offer_price', 'CHECK(offer_ids.price >= 0','Offer price must be greater than or equal to 0.'),
        ('check_tag_name_unique', 'UNIQUE(name)', 'Tag name must be unique.'),
        ('check_property_type_name_unique', 'UNIQUE(name)', 'Property type name must be unique.'),
    ]
    
    # Constraints
    @api.constrains('expected_price', 'selling_price')
    def _check_prices(self):
        for property in self :
            percet = float_compare((property.expected_price * 0.90), property.selling_price, precision_rounding=0.01)
            if percet > 0 and property.selling_price > 0:
                raise ValidationError("Selling price must be at least 90% of the expected price.")
            

    @api.onchange('state', 'offer_ids.status')
    def _check_offer_status(self):
        for property in self:
            if property.offer_ids == 'accepted':
                property.state = 'offer_accepted'
    
    @api.onchange('state')
    def _onchange_state(self):
        for property in self:
            if property.offer_ids and property.state == 'new':
                return property.state == 'offer_received'
                
    
    
    def unlink(self):
        for record in self:
            if record.state in ['sold', 'canceled']:
                raise UserError("Cannot delete a property that is sold or canceled.")
            record.offer_ids.unlink()
        return super().unlink()