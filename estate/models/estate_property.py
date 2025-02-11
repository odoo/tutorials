from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate property details"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description", required=True)
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From", copy=False, default=fields.Date.add(fields.Date.today(), months=3)) 
    expected_price = fields.Float(string="Expected Price")
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False) 
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"), 
            ("south", "South"), 
            ("east", "East"), 
            ("west", "West")
        ]
    )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        required=True,
        copy=False,
        default="new"
    )
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    user_id = fields.Many2one( "res.users", string="Salesperson",default=lambda self: self.env.user)
    partner_id = fields.Many2one("res.partner", string="Buyer", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    