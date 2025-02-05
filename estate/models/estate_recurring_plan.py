from odoo import fields, models
from datetime import datetime, timedelta  # Import required libraries

class RecurringPlan(models.Model):
    _name = "estate_property"
    _description = "Estate Recurring Plans"

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    
    # Default availability date to 3 months from today
    date_availability = fields.Date('Availability Date', copy=False, 
                                    default=lambda self: (datetime.today() + timedelta(days=90)).strftime('%Y-%m-%d'))
    
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', copy=False, readonly=True)
    
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    
    active = fields.Boolean('Active', default=True)

    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        default='new',  # Default state is 'New'
        required=True,   # Make this field required
        copy=False      # Do not copy this field when duplicating a record
    )

    property_type_id = fields.Many2one('property.type',string="Property Type")
    user_id = fields.Many2one('res.users', string='Salesperson',default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner',string='Buyer',copy=False)

    tag_ids = fields.many2many('property.tags',string='Tag',widget="many2many_tags")

