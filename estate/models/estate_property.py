from odoo import models, fields, api, exceptions
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_is_zero, float_compare


class EstateProperty(models.Model):

    _name = "estate.property"
    _description = "Estate property"
    _order = "id desc"

    name = fields.Char("Property Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Availability Date", copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))
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
        copy=False)

    active = fields.Boolean(default=True)

    type = fields.Many2one(comodel_name="estate.property.type")
    buyer = fields.Many2one(comodel_name="res.partner", copy=False)
    seller = fields.Many2one(string="Salesperson", comodel_name="res.users", default=lambda self: self.env.user)

    tags = fields.Many2many(comodel_name="estate.property.tag")

    offers = fields.One2many(comodel_name="estate.property.offer", inverse_name="property")

    total_area = fields.Integer(compute="_compute_total_area")

    best_price = fields.Float("Best offer price", compute="_compute_best_price")

    _expected_price_strictly_positive = models.Constraint(
        'CHECK(expected_price > 0)',
        'Expected price must be strictly positive'
    )
    _selling_price_strictly_positive = models.Constraint(
        'CHECK(selling_price > 0)',
        'Selling price must be strictly positive'
    )

    def _no_accepted_offer(self):
        return all(offer.state != "accepted" for offer in self.offers)

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for property in self:
            # No accepted offer and price is zero
            if float_is_zero(property.selling_price, 2) and property._no_accepted_offer():
                return

            if float_compare(property.selling_price, property.expected_price * 0.9, 2) == -1:
                raise exceptions.ValidationError(
                    "Selling price must be at least 90% of expected price. Update expected price to accept offer."
                )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offers")
    def _compute_best_price(self):
        for property in self:
            if not property.offers:
                property.best_price = 0
                continue
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

    def action_cancel_property(self):
        for property in self:
            if property.state == "sold":
                raise exceptions.UserError("Sold properties cannot be cancelled")
            property.state = "cancelled"
        return True

    def action_sell_property(self):
        for property in self:
            if property.state == "cancelled":
                raise exceptions.UserError("Cancelled properties cannot be sold")
            property.state = "sold"
        return True

    @api.ondelete(at_uninstall=False)
    def _unlink_only_new_cancelled(self):
        for property in self:
            if property.state != 'new' and property.state != 'cancelled':
                raise exceptions.UserError("You can only delete new or cancelled properties")
