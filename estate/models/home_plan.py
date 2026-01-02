from odoo import fields, models


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
    bedrooms = fields.Integer("bedrooms", default="2")
    living_area = fields.Integer("Living area")
    facades = fields.Integer("facades")
    Garage = fields.Boolean("Garage", default=True)
    Garden = fields.Boolean("Garden")
    Garden_area = fields.Integer("Garden area")
    active = fields.Boolean("Active", default=True)
    property_type_id = fields.Many2one("estate.property.type")
    Salesman = fields.Many2one("res.users", default=lambda self: self.env.user)
    Buyer = fields.Many2one("res.partner", copy=False)
    property_tag_id = fields.Many2many("estate.property.tag")
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

    # _sql_constraints = [
    #     ('check_number_of_months', 'CHECK(number_of_months >= 0)', 'The number of month can\'t be negative.'),
    # ]
