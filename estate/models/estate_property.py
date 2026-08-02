from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


class Property(models.Model):
    _name = "estate.property"
    _description = "Real Estate Properties"
    _order = "id desc"

    name = fields.Char(string='Title', required=True)

    description = fields.Text()

    postcode = fields.Char()

    date_availability = fields.Date('Available From', copy=False, default=(fields.Date.today() + relativedelta(months=3)))

    expected_price = fields.Float(required=True)

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The Expected Price must be strictly positive'
    )

    selling_price = fields.Float(readonly=True, copy=False)

    _check_selling_price = models.Constraint(
        'CHECK(selling_price > 0)',
        'The Selling Price must be strictly positive'
    )

    bedrooms = fields.Integer(default=2)

    living_area = fields.Integer(string="Living Area (sqm)")

    facades = fields.Integer()

    garage = fields.Boolean()

    garden = fields.Boolean()

    garden_area = fields.Integer(string="Garden Area (sqm)")

    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('west', 'West'),
            ('east', 'East'),
        ],
    )

    active = fields.Boolean(default=True)

    state = fields.Selection(
        string='Status',
        selection=[
            ('new', 'New'),
            ('received', 'Offer Received'),
            ('accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        required=True,
        copy=False,
        default="new"
    )

    property_type_id = fields.Many2one(comodel_name="estate.property.type")

    salesman_id = fields.Many2one(comodel_name="res.users", default=lambda self: self.env.uid)

    buyer_id = fields.Many2one(comodel_name="res.partner", copy=False)

    tag_ids = fields.Many2many(comodel_name="estate.property.tag")

    offer_ids = fields.One2many(comodel_name="estate.property.offer", inverse_name="property_id")

    total_area = fields.Integer(compute="_compute_total_area", string="Total Area (sqm)")

    best_offer = fields.Float(compute="_compute_best_offer")

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = record.offer_ids[0]['price'] if record.offer_ids else 0

    @api.onchange('garden')
    def _change_garden_fields(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    def _get_accepted_offers(self):
        return self.offer_ids.filtered(lambda offer: offer.status == 'accepted')

    @api.constrains('expected_price', 'selling_price')
    def _constraint_expected_selling_price(self):
        for record in self:
            if record.offer_ids and float_compare(record.expected_price * 0.9, record.selling_price, precision_digits=2) > 0:
                raise ValidationError(record.env._("Selling price must be at least %d%% of the expected price", 90))

    @api.ondelete(at_uninstall=False)
    def _prevent_deletion_of_new_or_cancelled_properties(self):
        for record in self:
            if record.state in {"new", "cancelled"}:
                raise UserError(self.env._("Cannot delete this property because it is 'New' or 'Cancelled'"))

    def _accept_offer(self, offer):
        self.ensure_one()
        if self._get_accepted_offers():
            return False

        self.state = 'accepted'
        self.selling_price = offer.price
        self.buyer_id = offer.partner_id

        return True

    def action_set_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(record.env._('Cancelled properties cannot be sold'))

            record.state = 'sold'

        return True

    def action_set_cancelled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(record.env._('Sold properties cannot be cancelled'))

            record.state = 'cancelled'

        return True
