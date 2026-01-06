from odoo import fields, models, api
from odoo.exceptions import UserError


class homePlan(models.Model):
    _name = "home.plan"
    _description = "this is home plan"

    name = fields.Char("Plan Name", required=True, default="Unknown")
    description = fields.Char("Description")
    postcode = fields.Char("Post code", required=True)
    date_availability = fields.Datetime(
        "Available till",
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3),
    )
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    expected_price = fields.Float("Expected Price")
    selling_price = fields.Float("Selling price", copy=False, readonly=True)
    bedrooms = fields.Integer("bedrooms", default=2)
    living_area = fields.Integer("Living area")
    facades = fields.Integer("facades")
    Garage = fields.Boolean("Garage", default=True)
    Garden = fields.Boolean("Garden")
    Garden_area = fields.Integer("Garden area", default=0)
    total_area = fields.Float("total area", compute="_compute_balance", store=True)
    best_price = fields.Float("best price", compute="_compute_offer")
    active = fields.Boolean("Active", default=True)
    property_type_id = fields.Many2one("estate.property.type")
    Salesman = fields.Many2one("res.users", default=lambda self: self.env.user)
    Buyer = fields.Many2one("res.partner", copy=False)
    property_tag_id = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")

    State = fields.Selection(
        [
            ("New", "new"),
            ("Offer Received", "offer received"),
            ("Offer Accepted", "offer accepted"),
            ("Sold", "sold"),
            ("Cancelled", "cancelled"),
        ],
        default="New",
        copy=False,
    )

    Garden_orientation_direction = fields.Selection(
        [("North", "north"), ("East", "east"), ("West", "west"), ("South", "south")]
    )

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)", "The expected price must be Strictly positive"
    )
    _check_selling_price = models.Constraint(
        "CHECK(selling_price > 0)", "The expected price must be Strictly positive"
    )

    @api.depends("living_area", "Garden_area")
    def _compute_balance(self):
        for line in self:
            line.total_area = line.living_area + line.Garden_area

    @api.depends("offer_ids")
    def _compute_offer(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("Garden")
    def _onchange_partner(self):
        for record in self:
            if record.Garden:
                record.Garden_area = 10
                record.Garden_orientation_direction = "East"

            else:
                record.Garden_area = 0
                record.Garden_orientation_direction = False

    def action_sold(self):
        for record in self:
            if record.State == "Cancelled":
                raise UserError(message="You can't sold once you have cancelled")
            else:
                record.State = "Sold"
        return True

    def action_Cancel(self):
        for record in self:
            if record.State == "Sold":
                raise UserError(message="You can't Cancel once you have sold")
            else:
                record.State = "Cancelled"

        return True
