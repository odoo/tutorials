from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, exceptions
from odoo.tools.float_utils import float_is_zero, float_compare

class Property(models.Model):

    # A bit ugly having this method on top, but if I move it on the bottom it gives me an error
    @staticmethod
    def in_3_months(*args):
        return date.today() + relativedelta(months=3)

    _name = "estate.property"
    _description = "Estate properties"

    _sql_constraints = [
        ('check_positive_prices', 'CHECK(expected_price > 0 AND selling_price > 0)',
         'A property expected price and selling price must be strictly positive.')
    ]

    _order = "id desc"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available From", copy=False, default=in_3_months)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
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
            ('east', 'East'),
            ('west', 'West')
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="Status",
        required=True,
        default='new',
        copy=False,
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ]
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if (not float_is_zero(record.selling_price, precision_digits=2) and
                float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0):
                raise exceptions.ValidationError("The selling price can't be lower than 90% of the expected price")


    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    # Naive solution
    # @api.depends("offer_ids.price")
    # def _compute_best_offer(self):
    #     for property in self:
    #         current_best = 0
    #         for offer in property.offer_ids:
    #             current_best = max(current_best, offer.price)
    #         property.best_offer = current_best

    # mapped() solution
    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(record.offer_ids.mapped("price"))
            else:
                record.best_offer = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_set_sold(self):
        if self.state == 'canceled':
            raise exceptions.UserError("Canceled properties cannot be sold")
        self.state = 'sold'
        return True

    def action_set_canceled(self):
        if self.state == 'sold':
            raise exceptions.UserError("Sold properties cannot be canceled")
        self.state = 'canceled'
        return True

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_canceled(self):
        if any(record.state not in ['new', 'canceled'] for record in self):
            raise exceptions.UserError("Only new or canceled properties can be deleted.")
