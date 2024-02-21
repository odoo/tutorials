from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare,float_is_zero


class Property(models.Model):
    _name = "estate.property"
    _description = "Real Estate Application"

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'A property expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'A property selling price must be positive.'),
    ]

    name = fields.Char(string="Title", required=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    user_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
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
            ("west", "West"),
        ],
    )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        copy=False,
        required=True,
        default="new",
        string="Status",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
    )
    total_living_area = fields.Integer(compute="_calculate_total_area")
    best_price = fields.Float(compute="_get_max_offer")


    @api.depends("living_area", "garden_area")
    def _calculate_total_area(self):
        for record in self:
            record.total_living_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _get_max_offer(self):
        for record in self:
            record.best_price = (
                max(record.offer_ids.mapped("price")) if record.offer_ids else 0
            )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
            return
        self.garden_area=0
        self.garden_orientation=None
        

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price,1):
                continue
            if float_compare(record.selling_price/record.expected_price, 0.9, 1) < 0:
                raise ValidationError("The selling price is less than 90% of the expected price")

    def action_sold_property(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("Canceled properties cannot be sold")
            record.state = "sold"
        return True

    def action_cancel_property(self):
        for record in self:
            if record.state == "sold":
                raise UserError("sold properties cannot be canceled")
            record.state = "canceled"
        return True
