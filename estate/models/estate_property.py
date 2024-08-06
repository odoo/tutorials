from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):

    _name = "estate.property"
    _description = "Estate property"

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Date Availability', copy=False, default=(
        date.today() + relativedelta(months=3)))
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area ')
    garden_orientation = fields.Selection(string='Garden Orientation',
                                          selection=[
                                              ('north', 'North'),
                                              ('south', "South"),
                                              ('east', 'East'),
                                              ('west', 'West'),
                                          ]
                                          )
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection(string='Status',
                             selection=[
                                 ('new', 'New'),
                                 ('offer received', 'Offer Received'),
                                 ('offer accepted', 'Offer Accepted'),
                                 ('sold', 'Sold'),
                                 ('cancelled', 'Cancelled')
                             ]
                             )
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type", string="Property Type")
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Buyer", copy=False)
    user_id = fields.Many2one(
        comodel_name="res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many(
        comodel_name="estate.property.tag", string="Tages")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(string="Total area", compute="_compute_values")
    best_price = fields.Float(string="Best offer", compute="_compute_values")

    @api.depends("garden_area", "living_area", "offer_ids.price")
    def _compute_values(self):
        for record in self:
            # for calculating total_area
            record.total_area = record.garden_area + record.living_area

            # for calculating best_price
            record.best_price = max(record.offer_ids.mapped(
                "price")) if record.offer_ids else 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""
