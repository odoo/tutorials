from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Property'
    _inherit = ['mail.thread']

    name = fields.Char(string="Property Name", required=True)
    image = fields.Binary(string="Image")
    company_id = fields.Many2one(
        'res.company',
        required=True,
        default=lambda self: self.env.company
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    property_tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Property Offers", tracking=True)

    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Available From",
        default=lambda self: date.today() + relativedelta(months=+3),
        copy=False
    )

    expected_price = fields.Float(string="Expected Price", required=True, default=0.0)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)

    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Has Garage")
    garden = fields.Boolean(string="Has Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation"
    )

    salesperson_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False, tracking=True)

    status = fields.Selection(
        [('new', 'New'), ('offer_received', 'Offer Received'),
         ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        string="Status",
        default='new',
        readonly=True,
        copy=False,
        tracking=True
    )

    total_area = fields.Float(compute="_compute_total_area", readonly=True)
    best_price = fields.Float(compute="_compute_best_price", readonly=True, default=0.0)

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be greater than 0.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be non-negative.')
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.constrains('selling_price')
    def check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            min_price = record.expected_price * 0.9
            if float_compare(record.selling_price, min_price, precision_digits=2) == -1:
                raise ValidationError("Selling price cannot be less than 90% of the expected price.")

    @api.constrains("offer_ids")
    def _set_status_to_offer_received(self):
        for record in self:
            record.status = "offer_received" if record.offer_ids and record.status == "new" else record.status
            if not record.offer_ids:
                record.status = "new"

    def set_sold(self):
        for record in self:
            if record.status == "cancelled":
                raise ValidationError("Cancelled properties cannot be sold.")

            if not record.offer_ids:
                raise ValidationError("No offers available to mark the property as sold.")

            accepted_offer = record.offer_ids.filtered(lambda o: o.status == "accepted")
            if not accepted_offer:
                raise ValidationError("Accept an offer before selling the property.")

            record.status = "sold"
        return True

    def set_cancel(self):
        for record in self:
            record.status = "cancelled"
            record.offer_ids.write({'status': 'refused'})
        return True
