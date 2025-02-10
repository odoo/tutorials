from dateutil.relativedelta import relativedelta
from odoo import models , fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "This is property tabel."

    name = fields.Char("Property Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(string="Available From", copy=False, default=fields.Date.today()+relativedelta(months=3))
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection( 
        string="Garden Orientation",
        selection=[
            ('north', 'North'), 
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ])
    active = fields.Boolean(string="Active",default=False)
    state = fields.Selection(
        string="State",
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        required=True,
        copy=False,
        default='new'
    )
    property_type_id = fields.Many2one("estate.property.type" , string="Property Type")
    buyer_id = fields.Many2one("res.partner" , string="Buyers" , copy=False)
    seller_id = fields.Many2one("res.users" ,default=lambda self : self.env.user, string="Sellers")
    tag_ids = fields.Many2many(comodel_name="estate.property.tag" ,relation="property_tag_rel" ,string="Tags")
    offer_ids = fields.One2many(comodel_name="estate.property.offer" ,inverse_name="property_id" ,string="Offers")
