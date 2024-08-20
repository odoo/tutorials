from dateutil.relativedelta import relativedelta
from datetime import date
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property Data"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    name = fields.Char(required=True)
    description = fields.Char()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=date.today() + relativedelta(months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean(default=True)
    state = fields.Selection(
        required=True,
        copy=False,
        default="new",
        selection=[
            ("new", "New"),
            ("offer_recived", "Offer Recieved"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        tracking=True,
    )
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )
    _order = "id desc"
    salesman_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user,
    )
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False,
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags", ondelete="cascade")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total = fields.Integer(compute="total_area")
    best_offer = fields.Float(compute="best_offer_selete", store=True)
    property_type_id = fields.Many2one("estate.property.type")
    sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "The Expected Price of Property should be positive",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0 )",
            "The Selling Price of Property should be Positive",
        ),
        ("name_uniq", "unique (name)", "Property name already exists!"),
    ]

    @api.depends("living_area", "garden_area")
    def total_area(self):
        for recorde in self:
            recorde.total = recorde.living_area + recorde.garden_area

    @api.depends("offer_ids")
    def best_offer_selete(self):
        temp = 0
        for offer in self.offer_ids:
            if offer.price > temp:
                temp = offer.price
        self.best_offer = temp

    @api.onchange("garden")
    def garden_change(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def status_action_sold_button(self):
        if self.state == "canceled":
            raise UserError("Canceled property can't be sold")
        else:
            self.state = "sold"

    def status_action_canceled_button(self):
        if self.state == "sold":
            raise UserError("Sold property can't be canceled")
        else:
            self.state = "canceled"

    @api.constrains("selling_price", "expected_price")
    def _check_date_end(self):
        for record in self:
            if record.selling_price > 0:
                price_percent = (record.selling_price / record.expected_price) * 100
                if price_percent < 90:
                    raise ValidationError("Selling Price must be at least 90%")

    @api.ondelete(at_uninstall=False)
    def _check_property_state(self):
        for recod in self:
            if recod.state == "new" or recod.state == "canceled":
                continue
            else:
                raise ValidationError("New or Canceled property can be delete only.")
