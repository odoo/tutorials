from odoo import fields, models
from odoo.tools import relativedelta

class EstateProperty(models.Model):
    # Table meta-data
    _name = "estate.property"
    _description = "Estate Property"

    # Table relations
    # Many2one or One2Many
    property_type_id = fields.Many2one(string="Property Type", comodel_name="estate.property.type")
    salesperson_id = fields.Many2one(string="Salesperson", comodel_name="res.users", default=lambda self: self.env.user)
    buyer_id = fields.Many2one(string="Buyer", comodel_name="res.partner", copy=False)
    # Many2Many
    tag_ids = fields.Many2many(string="Tags", comodel_name="estate.property.tag")
    # One2Many
    offer_ids = fields.One2many(string="Offers", comodel_name="estate.property.offer", inverse_name="property_id")
    
    #Table attributes
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(default=lambda self: fields.Date.today() + relativedelta(months=3), copy=False, string="Available From")
    expected_price = fields.Float(required=True, string="Expected Price")
    selling_price = fields.Float(readonly=True, copy=False, string="Selling Price")
    active = fields.Boolean(default=True, string="Active")

    bedrooms = fields.Integer(default=2, string="Bedrooms")
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], string="Garden Orientation")
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
    ], default='new', required=True, copy=False, string="State")
