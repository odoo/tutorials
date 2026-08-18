from odoo import models, fields, api
from dateutil import relativedelta


class EstateProperty(models.Model):

    _name = "estate.property"
    _description = "Estate property"

    name = fields.Char("Property Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Availability Date", copy=False, default=lambda self:fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer("Number of Bedrooms", default=2)
    living_area = fields.Integer("Living Area m²")
    facades = fields.Integer("Number of Facades")
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area m²")
    garden_orientation = fields.Selection(selection=[('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')])
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'), ('cancelled', 'Cancelled'),
        ],
        default='new',
        required=True,
        copy=False,)

    active = fields.Boolean(default=True)

    type = fields.Many2one(comodel_name="estate.property.type")
    buyer = fields.Many2one(comodel_name="res.partner", copy=False)
    seller = fields.Many2one(string="Salesperson", comodel_name="res.users", default=lambda self: self.env.user)

    tags = fields.Many2many(comodel_name="estate.property.tag")

    offers = fields.One2many(comodel_name="estate.property.offer", inverse_name="property")

    total_area = fields.Integer(compute="_compute_total_area")

    best_price = fields.Float("Best offer price", compute="_compute_best_price")


    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offers")
    def _compute_best_price(self):
        for property in self:
            best_offer = max(property.offers, key=lambda offer: offer.price)
            property.best_price = best_offer.price

    @api.onchange("garden")
    def _onchange_garden(self):
        for property in self:
            if property.garden:
                property.garden_area = 10
                property.garden_orientation = 'north'
            else:
                property.garden_area = None
                property.garden_orientation = None
