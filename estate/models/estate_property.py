from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "total_area asc"

    name = fields.Char(
        required=True,
    )
    description = fields.Text()
    postcode = fields.Char(required=True)
    available_from = fields.Date(
        string="Availble From",
        copy=False,
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    facades = fields.Integer(default=0)
    living_area = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean(default=True)
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)", "The expected price must be strictly positive"
    )
    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)", "The selling price must be strictly positive"
    )
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        copy=False,
        readonly=True,
        default="new",
    )

    total_area = fields.Float(compute="_compute_total_area", readonly=False, store=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", readonly=True, copy=False)
    user_id = fields.Many2one(
        "res.users", string="SalesPerson", default=lambda self: self.env.user
    )

    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="offers",
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    maintenance_ids = fields.One2many(
        "estate.property.maintenance", "property_id", string="Maintenance"
    )

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        for record in self:
            offers = record.offer_ids
            if not offers:
                raise UserError("offers should be created first to get sold")
            if record.state == "cancelled":
                raise UserError("Cancelled property cannot be sold.")
            record.state = "sold"

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold property cannot be cancelled.")
            record.state = "cancelled"
        return True   

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for prop in self:
            if float_is_zero(prop.selling_price, precision_digits=2):
                continue
            minimum_price = prop.expected_price * 0.9
            if float_compare(prop.selling_price, minimum_price, precision_digits=2) < 0:
                raise ValidationError(
                    "The selling price cannot be lower than 90 percent of the expected price."
                )

    @api.ondelete(at_uninstall=False)
    def _check_before_deleting(self):
        for record in self:
            if record.state not in ("new", "cancelled"):
                raise UserError(
                    "you cannot delete a property unless it is New or Cancelled"
                )
    

    def best_offer(self):
        for record in self:
            offers = record.offer_ids
            if offers:
                max_price = max(offers.mapped("price"))   

            else:
                raise UserError("offer should be created for finding best offer")

            best_offered_price = offers.filtered(lambda offer : offer.price == max_price)

            if best_offered_price:
                for offer in best_offered_price:
                    offer.accept_offer()
                record.action_sold()
