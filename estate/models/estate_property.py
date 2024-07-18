
from odoo import models,fields,api
from datetime import datetime, timedelta

class EstateProperty(models.Model):
    
    _name = "estate.property"
    _description = 'Property the estate'
    _inherit = "estate.property"
    _order = "id desc"

    name = fields.Char(string='Property Name', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Availability Date', default=lambda self: datetime.today() + timedelta(days=90))
    selling_price = fields.Float(string='Selling Price')
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_orientation = fields.Selection(string='Garden Orientation',selection = [('north','North'),('soul','South'),('east','East'),('west','West')])
    orientation = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
    ], string='Orientation', required=True, default='new'),
    property_type_id = fields.Many2one('estate.property.type', string='Property Type', no_create_edit=True)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute='_compute_total_area', string='Total Area')
    best_price = fields.Float(compute='_compute_best_price', string='Best Offer')       
    state = fields.Selection(selection_add=[('canceled', 'Canceled'), ('sold', 'Sold')])

    

@api.onchange('garden')
def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.orientation = 'North'
        else:
            self.garden_area = 0
            self.orientation = False


def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

def _compute_best_price(self):
        for record in self:
            offers = record.offer_ids
            if offers:
                record.best_price = max(offers.mapped('price'))
            else:
                record.best_price = 0.0

def cancel_property(self):
        if self.state == 'old':
            raise UserError("A sold property cannot be canceled")
        self.state = 'canceled'

def set_sold(self):
        if self.state == 'canceled':
            raise UserError("A canceled property cannot be set as sold")
        self.state = 'old'


@api.model
def create(self, vals):
       
        property_id = vals.get('property_id')
        property = self.env['estate.property'].browse(property_id)
        property.state = 'offer_received'

        existing_offers = self.env['estate.property.offer'].search([('property_id', '=', property_id)])
        if existing_offers:
            max_offer_amount = max(existing_offers.mapped('price'))
            if vals.get('price') <= max_offer_amount:
                raise ValueError("Offer amount must be higher than existing offers")

        return super(EstatePropertyOffer, self).create(vals)

@api.multi
def unlink(self):
        
        for record in self:
            property = record.property_id
            if property.state not in ['new', 'canceled']:
                raise UserError("Cannot delete an offer for a property that is not in 'New' or 'Canceled' state")
        return super(EstatePropertyOffer, self).unlink()

@api.ondelete(at_unlink=True, model='estate.property')
def _prevent_deletion_if_offers_exist(self):

        for property in self:
            if property.offer_ids:
                raise UserError("Cannot delete a property that has offers")



class Property(models.Model):
    _name = 'property'

    expected_price = fields.Float(string='Expected Price')
    selling_price = fields.Float(string='Selling Price')

    _sql_constraints = [
        ('expected_price_positive', 'CHECK(expected_price > 0)', 'Expected price must be strictly positive'),
    ]
    _sql_constraints = [
        ('selling_price_positive', 'CHECK(selling_price >= 0)', 'Selling price must be positive'),
    ]

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0:
                    raise ValidationError(_('Selling price cannot be lower than 90% of the expected price'))