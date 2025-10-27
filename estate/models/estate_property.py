from datetime import date

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char(string="Title", required=True)
    property_type = fields.Selection(
        string='Property Type',
        selection=[('house', 'House'), ('apartment', 'Apartment')])
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, readonly=True, default=lambda self: date.today() + relativedelta(months=3))
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (m2)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area (m2)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'),
        ('east', 'East'), ('west', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection(
        copy=False,
        readonly=True,
        default='new',
        string='Property_States',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')]
    )

    property_type_id = fields.Many2one('estate.property.type', string='Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesman_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    tags_ids = fields.Many2many('estate.property.tags', string='Tags')
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="offer")
    total_area = fields.Integer(string='Total Area(m2)', compute='_compute_total_area', store=True)
    best_price = fields.Float(string='Best Offer', compute='_compute_best_price', store=True)

    _check_expected_price = models.Constraint(
         'CHECK(expected_price >= 0)', 'The expected price must be strictly positive.')

    _check_selling_price = models.Constraint(
         'CHECK(selling_price > 0)', 'The selling price must be positive.')

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_expected_price(self):
        for record in self:
            if record.selling_price == 0:
                continue
            if float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) == -1:
                raise UserError("The selling price must be at least 90% of the expected price.")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
             property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
                record.best_price = max(record.offer_ids.mapped('price')) if record.offer_ids else 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.onchange('offer_ids')
    def _onchange_offers(self):
        for record in self:
            has_offers = any(offer.status not in ('refused', 'accepted') for offer in record.offer_ids)
            if record.state == 'new' and has_offers:
                record.state = 'offer_received'

            if not has_offers and not any(offer.status == 'accepted' for offer in record.offer_ids) and record.state in ('offer_received',):
                record.state = 'offer_receive'

    @api.ondelete(at_uninstall=False)
    def _if_new_or_canceled(self):
        if not set(self.mapped("state")) <= {"new", "canceled"}:
            raise UserError("Only new and canceled properties can be deleted.")

    def action_set_sold(self):
        print(self.state)
        if self.state == "cancelled":
            raise UserError("A cancelled property can not be sold")
        self.state = "sold"
        return True

    def action_set_cancelled(self):
        if self.state == "sold":
            raise UserError("A sold property can not be cancelled")
        self.state = "cancelled"
        return True
