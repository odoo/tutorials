from odoo import models, fields
from datetime import timedelta

class EstateProperties(models.Model):
    _name = "estate.property"
    _description = "estate properties"

    name = fields.Char("Name", readonly=False, required=True)
    description = fields.Text("Description", readonly=False)
    
    postcode = fields.Char("Postcode", readonly=False)
    date_availability = fields.Date("Available From", readonly=False, copy=False, default=lambda self: fields.Date.today() + timedelta(days=90))
    
    expected_price = fields.Float("Expected Price", readonly=False, required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    
    bedrooms = fields.Integer("Bedrooms", readonly=False, default=2)
    living_area = fields.Integer("Living Area", readonly=False)
    
    facades = fields.Integer("Facades", readonly=False)
    
    garage = fields.Boolean("Garage", readonly=False)
    garden = fields.Boolean("Garden", readonly=False)
    garden_area = fields.Integer("Garden Area", readonly=False)
    
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help = "The garden orientation is used to describe Garden's orientation, lol?"
    )

    active = fields.Boolean("Active", default=True)

    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        default="new",
        string="Status",
        required=True
    )

    # seller = fields.Char("Seller", readonly=False)
    # buyer = fields.Char("Buyer", eadonly=False)

    seller_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)

    property_type_id = fields.Many2one("estate.property.type", string="Type")
    property_tags_id = fields.Many2many("estate.property.tag", string="Tags")

    offer_ids = fields.One2many("estate.property.offer", inverse_name="property_id")
    
