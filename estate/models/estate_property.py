from odoo import api, fields, models
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    # _order = ... ?


    name = fields.Char('Property Name', required=True, translate=True)
    description = fields.Text('Description', translate=True)
    postcode = fields.Char('Post Code', required=True)
    date_availability = fields.Date(
        'Availability Date', 
        required=True, 
        copy=False,
        default=fields.Date.today() + relativedelta(months=3)
    )
    
    type_id = fields.Many2one("estate.property.type", string="Type", required=True)
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson", 
        default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one(
        "res.partner", 
        string="Buyer",
        copy=False
    )

    expected_price = fields.Float('Expected Price')
    selling_price = fields.Float(
        'Selling Price', 
        readonly=True, 
        copy=False
    )

    bedrooms = fields.Integer(
        '# Bedrooms', 
        default=2
    )
    facades = fields.Integer('# Facades')

    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')

    living_area = fields.Integer('Living Area mt²')
    garden_area = fields.Integer('Garden mt²')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ] 
    )

    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'),
            ('offer', 'Offer'),
            ('received', 'Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        default="new",
        copy=False,
        required=True
    )

    total_area = fields.Integer(
        "Total Area m²",
        compute="_compute_total_area",
        readonly=True
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

