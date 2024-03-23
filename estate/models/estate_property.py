from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True, string="Title")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(default=fields.Date.add(fields.Date.today(), months=3), copy=False, string="Available From")
    expected_price = fields.Float(required=True, string="Expected Price")
    selling_price = fields.Float(readonly=True, copy=False, string="Selling Price")
    bedrooms = fields.Integer(default=2, string="Bedrooms")
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
        help="Type to detect orientation of the garden")
    active = fields.Boolean(default=True)
    state = fields.Selection(
        default='new',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')])
    salesperson = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    buyer = fields.Many2one("res.partner", copy=False, string="Buyer")
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
