
from odoo import models,fields,api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Management Module"

    name = fields.Char('Property Name', required=True)
    description=fields.Text('Description' )
    postcode = fields.Char('Postcode')
    date_availability=fields.Date( 'Available From', copy=False, default= (datetime.today() + relativedelta(months=3)).date())
    
    
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)

    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')

    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection( 
                selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
                string='Garden Orientation') 

    active=fields.Boolean(default=True)
    # last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)


    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        string='State',
        required=True,
        default='new',  
        copy=False,  
    )

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    user_id = fields.Many2one('res.users', string='Salesman', index=True, tracking=True, default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string='Buyer', index=True, tracking=True, default=lambda self: self.env.user)

    tag_ids=fields.Many2many("estate.property.tag", string="Property Tags")

    offer_ids = fields.One2many(
        comodel_name='estate.property.offer',  
        inverse_name='property_id',  
        string='Offers'  
    )
    
    
    total_area = fields.Float(compute="_compute_total_area")

    @api.depends("garden_area","living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area