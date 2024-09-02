from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare
from dateutil.relativedelta import relativedelta
from datetime import date


class EstateProperty(models.Model):

    _name = "estate.property"
    _description = "estate property description"
    _order = "id desc"

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date Availability', copy=False, default=(
        date.today() + relativedelta(months=3)))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('living_area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    property_type_id = fields.Many2one(
        'estate.property.type', string='Property Type')
    buyer = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson = fields.Many2one(
        'res.users', string='SalesPerson', default=lambda self: self.env.user)
    garden_orientation = fields.Selection(string='Garden Orientation',
                                          selection=[
                                              ('north', 'North'),
                                              ('south', "South"),
                                              ('east', 'East'),
                                              ('west', 'West'),
                                          ])
    active = fields.Boolean(default=True)
    state = fields.Selection(string='Status', required=True, copy=False, default='new',
                             selection=[
                                 ('new', 'New'),
                                 ('offer Received', 'Offer Received'),
                                 ('offer Accepted', 'Offer Accepted'),
                                 ('sold', 'Sold'),
                                 ('canceled', 'Canceled')
                             ]
                             )

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many(
        'estate.property.offer', "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total")
    best_price = fields.Float(
        compute="_compute_best_price", string="Best offer")
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The expected price must be strictly positive and greater than zero'),
        ('check_selling_price', 'CHECK(selling_price >=0)',
         'The selling price should not be negative')
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(
                    record.offer_ids.mapped('price'), default=0.0)
            else:
                record.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_sold(self):
        if self.state == "canceled":
            raise UserError(_("cancelled property cannot be sold"))
        else:
            self.state = 'sold'

    def action_cancel(self):
        if self.state == 'sold':
            raise UserError(_("sold property cannot be canceled"))
        else:
            self.state = 'canceled'

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=6) == - 1:
                raise ValidationError(
                    "the selling price cannot be lower than 90% the expected price")

    @api.ondelete(at_uninstall=False)
    def _unlink_except_new_canceled(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise UserError(
                    "You cannot delete a property unless its state is 'New' or 'Canceled'.")
