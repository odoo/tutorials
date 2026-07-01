from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3), string="Availability Date")
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(readonly=True, copy=False, string="Selling Price")
    bedrooms = fields.Integer(default=2, string="Bedrooms")
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garage_area = fields.Integer(string="Garage Area")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    active = fields.Boolean(default=True, string="Active")
    total_area = fields.Integer(string="Total Area", compute="_compute_total_area")

    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        required=True,
        copy=False,
        default='new',
        string="State"
    )
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        string="Garden Orientation"
    )

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", default=lambda self: self.env.user, string="Salesperson")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_price = fields.Integer(string="Best price", compute="_compute_best_price", store="True")

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            price = record.offer_ids.mapped('price')
            record.best_price = max(price) if price else 0.0

    @api.onchange('garden')
    def _on_change_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.onchange('garage')
    def _on_change_garage(self):
        if self.garage:
            self.garage_area = 10
        else:
            self.garage_area = 0

    @api.depends('living_area', 'garden_area', 'garage_area')
    def _compute_total_area(self):
        # breakpoint()
        for record in self:
            record.total_area = record.living_area + record.garden_area + record.garage_area
