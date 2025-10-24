from odoo import models, fields, api, exceptions
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Properties"
    _order = "id desc"

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price must be strictly positive.',
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price must be positive.',
    )

    ####################################################
    # FIELDS DECLARATION
    ####################################################

    name = fields.Char(
        string='Title',
        required=True,
        default="My new house"
    )
    description = fields.Text()
    notes = fields.Html()
    postcode = fields.Char()
    date_availability = fields.Date(
        string='Available From',
        default=fields.Date.add(fields.Date.today(), months=3),
        copy=False
    )
    expected_price = fields.Float(string='Expected price', required=True)
    selling_price = fields.Float(
        readonly=True,
        copy=False
    )
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        default='new'
    )
    property_type_id = fields.Many2one("estate.property.type")
    partner_id = fields.Many2one("res.partner", string="Buyer")
    user_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id"
    )
    total_area = fields.Float(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_price")

    ####################################################
    # FUNCTIONS DECLARATION
    ####################################################

    def cancel_property_button(self):
        self.ensure_one()
        if self.state != "sold":
            self.state = "canceled"
        else:
            raise exceptions.UserError("Sold properties cannot be canceled")
        return True

    def sold_property_button(self):
        self.ensure_one()
        if self.state != "canceled":
            self.state = "sold"
        else:
            raise exceptions.UserError("Canceled properties cannot be sold")
        return True

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price')) if record.offer_ids else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if not self.garden:
            self.garden_orientation = "north"
            self.garden_area = 10

    @api.constrains("state")
    def _check_offers_state(self):
        self.ensure_one()
        if self.state == 'sold' and not [offer for offer in self.offer_ids if offer.status == 'accepted']:
            raise exceptions.UserError("You cannot sold a property without accepted offer")

    @api.constrains('selling_price', 'expected_price')
    def _check_date_end(self):
        for record in self:
            if float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) < 0 and record.selling_price > 0:
                raise exceptions.ValidationError(
                    r"The selling price must be at least 90% of the expected price! You must reduce the expected price if you want to accept this offer."
                )

    ####################################################
    # CRUD
    ####################################################

    @api.ondelete(at_uninstall=False)
    def _unlink_if_offer_unavailable(self):
        if self.state not in ['new', 'canceled']:
            raise exceptions.UserError("Can't delete an active property!")
