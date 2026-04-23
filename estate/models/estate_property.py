from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class Estate_property(models.Model):
    _name = "estate_property"
    _description = "APP super mega trop bien"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="The garden orientation",
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="Status",
        selection=[('new', 'New'), ('offer Received', 'Offer Received'), ('offer Accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        required=True,
        copy=False,
        default="new",
        compute="_compute_state",
        store=True,
    )
    property_type_id = fields.Many2one("estate_property_type", string="Property Type")
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate_property_tag", string="Tags")
    offer_ids = fields.One2many("estate_property_offer", "property_id", string="Offers")
    total_area = fields.Integer(compute="_compute_area")
    best_price = fields.Float(compute="_compute_best_price")

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        message="The expected price must be strictly positive",
    )

    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)",
        message="The selling price cannot be negative",
    )

    @api.depends("living_area", "garden_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.depends("offer_ids", "offer_ids.state")
    def _compute_state(self):
        if self.state in ["sold", "cancelled"]:
            return
        if self.offer_ids:
            self.state = "offer Received"
            for offer in self.offer_ids:
                if offer.state == "accepted":
                    self.state = "offer Accepted"
                    break
        else:
            self.state = "new"
            self.selling_price = 0

    def action_sold(self):
        for record in self:
            if record.state != "cancelled" and record.state != "sold":
                record.state = "sold"
            else:
                raise UserError("A property that is cancelled or already sold cannot be sold.")

    def action_cancel(self):
        for record in self:
            if record.state != "sold" and record.state != "cancelled":
                record.state = "cancelled"
            else:
                raise UserError("A property that is sold or already cancelled cannot be cancelled.")

    @api.constrains("selling_price", "expected_price")
    def _check_enough_selling_price(self):
        for record in self:
            if record.selling_price and record.selling_price < record.expected_price * 0.9:
                raise ValidationError("The selling price cannot be less than 90% of the expected price.")
