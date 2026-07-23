from odoo import fields, models, api
from datetime import timedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Module"

    # Base Fields

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", copy=False, readonly=True)
    best_price = fields.Integer(string="Best Price", compute="_compute_best_price")
    expected_date = fields.Date(
        string="Expected Date",
        required=True,
        copy=False,
        default=(fields.Date.today() + timedelta(days=90)),
    )
    bedroom = fields.Integer(string="Number of Bedroom", default=2)
    living_area = fields.Integer(string="Living area (square metter)")
    facades = fields.Integer(string="Number of facades")
    garage = fields.Boolean(string="Have a garage?")
    garden = fields.Boolean(string="Have a garden?")
    garden_area = fields.Integer(string="Garden area (square metter)")
    garden_orientation = fields.Selection(
        string="Garden's orientation",
        selection=[
            ("north", "North"),
            ("sud", "Sud"),
            ("east", " East"),
            ("west", "West"),
        ],
    )
    total_area = fields.Integer(string="Total Area", compute="_compute_total_area")
    state = fields.Selection(
        string="Estate's state",
        selection=[
            ("new", "New"),
            ("offer_recieved", "Offer Received"),
            ("offer_accepted", " Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
    )
    salesman_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    property_tag_ids = fields.Many2many("estate.property.tag", string="Tag")
    proterty_offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    active = fields.Boolean(default=True)


    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('proterty_offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            prices = record.proterty_offer_ids.mapped('price')
            if not prices:
                record.best_price = 0
            else:
                record.best_price = max(prices)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''
        # return {'warning': {'title': "Test warning", 'message': "foo", 'type': 'notification'},}
