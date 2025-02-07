from datetime import timedelta

from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Date availability", copy=False, default=fields.Date.today() + timedelta(days=+90))
    expected_price = fields.Float(string="Expected price", required=True)
    selling_price = fields.Float(string="Selling price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living area")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [('north','North'),
         ('south','South'),
         ('east','East'),
         ('west','West')],
        string = "Garden Orientation", help = "It is used to define the garden orientation"
    )
    state = fields.Selection(
        [('new', 'New'),
         ('offerreceived', 'Offer Received'),
         ('offeraccepted', 'Offer Accepted'), 
         ('sold', 'Sold'), 
         ('cancelled', 'Cancelled')
        ],
        string="State", default = "new"
    )
    active = fields.Boolean("Active", default=True)
    seller = fields.Many2one(comodel_name="res.users", string="Salesperson", default=lambda self: self.env.user)
    buyer = fields.Many2one(comodel_name="res.partner", string="Buyer", copy=False)
    property_type_id = fields.Many2one(comodel_name="estate.property.type", string="Property Type")
    tag_ids = fields.Many2many(comodel_name="estate.property.tag", string="Tags")
    offer_ids = fields.One2many(comodel_name="estate.property.offer", inverse_name="property_id")
