
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo import tools

class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char('Name', required=True, translate=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date Availability', copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=2))
    expected_price = fields.Float('Expected Price', required=True)
    _positive_expected_price = models.Constraint("CHECK(expected_price > 0)", "Expected price must be positive.")
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    _positive_selling_price = models.Constraint("CHECK(selling_price >= 0)", "Selling price must be positive.")
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Orientation of the garden")
    state = fields.Selection(
        string='Status',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'),
                   ('sold', 'Sold'), ('canceled', 'Canceled')],
        required=True, copy=False, default='new')

    property_type_id = fields.Many2one('estate_property_type', string='Property Type')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    salesman_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)

    tag_ids = fields.Many2many('estate_property_tag', string='Tags')
    offer_ids = fields.One2many('estate_property_offer', 'property_id', string='Offers')

    total_area = fields.Integer('Total Area', compute='_compute_total_area')

    best_price = fields.Float('Best Offer', compute='_compute_best_price')

    active = fields.Boolean('Active', default=True)
    sequence = fields.Integer('Sequence', default=10)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_cancel_estate_property(self):
        if self.state == 'sold':
            raise UserError("You cannot cancel a sold property.")
        for record in self:
            record.state = 'canceled'
        return True

    def action_sold_estate_property(self):
        if not any(self.offer_ids.mapped(lambda offer: offer.status == 'accepted')):
            raise UserError("You cannot sell a property with no accepted offers.")
        if self.state == 'canceled':
            raise UserError("You cannot sell a canceled property.")
        for record in self:
            record.state = 'sold'
        return True

    @api.constrains('selling_price')
    def _check_selling_price_to_expected(self):
        for record in self:
            if record.selling_price == 0:
                continue
            if tools.float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0:
                raise ValidationError("The selling price cannot be lower than the expected price")
        # all records passed the test, don't return anything

    @api.model
    def ondelete(self, records):
        for record in records:
            if record.state not in ['new', 'canceled']:
                raise UserError("You cannot delete a property that is not new or canceled.")
        return super().ondelete(records)
