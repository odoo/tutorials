from odoo import fields, models
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name='estate.property'
    _description="Real Estate Property"

    name=fields.Char('Title', required=True, translate=True)
    property_type_id=fields.Many2one(
        'estate.property.type',
        string='Property Type',
    )
    postcode=fields.Char('Postcode', required=True)
    availability =fields.Date(
        'Available From', 
        required=True, 
        copy=False, 
        default=lambda self: fields.Date.today()+relativedelta(months=3),
    )
    description=fields.Text('Description')
    bedrooms=fields.Integer('Bedrooms', required=True, default=2)
    living_area=fields.Integer('Living Area (sqm)', required=True)
    currency_id=fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id.id)
    expected_price=fields.Monetary('Expected Price', required=True)
    selling_price=fields.Monetary('Selling Price', readonly=True, copy=False)
   # best_offer_id = fields.Many2one('estate.property.offer', string='Best Offer', readonly=True)
    facades=fields.Integer('Facades', default=False)
    garage=fields.Boolean('Garage', default=False)
    garden=fields.Boolean('Garden', default=False)
    garden_area=fields.Integer('Garden Area (sqm)', required=False)
    garden_orientation=fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string='Garden Orientation'
    )
    total_area=fields.Integer('Total Area (sqm)')

    state=fields.Selection(
        string ='Status',
        selection =[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'),
         ('sold', 'Sold'), ('canceled', 'Canceled')],
        required=True,
        copy=False,
        default='new',
    )
    active =fields.Boolean('Active', default=True)
    buyer_id =fields.Many2one('res.partner', string='Buyer', copy=False)
    seller_id=fields.Many2one('res.users', string='Salesperson', default=lambda self:self.env.user)

    # _check_expected_price = models.Constraint(
    #     'CHECK(expected_price) >= 0',
    #     "The expected price can't be negative",
    # )
