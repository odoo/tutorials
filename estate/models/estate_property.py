from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Real Estate Property"
    _order = "id desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The property expected price must be strictly positive',
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The property selling price must be positive',
    )

    name = fields.Char(string="Property Name", required=True, help='Enter the name of the property')
    image = fields.Image(string="Property Image", max_width=1024, max_height=1024)
    description = fields.Text(string="Property Description", help='Enter a description of the property')
    postcode = fields.Char(string="Postcode", help='Enter the postcode of the property')
    date_availability = fields.Date(
        string="Availability Date",
        help='Enter the date when the property becomes available',
        copy=False,
        default=lambda self: fields.Date.today() + relativedelta(months=3)
    )
    expected_price = fields.Float(string="Expected Price", required=True, help='Enter the expected price of the property')
    selling_price = fields.Float(string="Selling Price", help='Enter the selling price of the property', readonly=True, copy=False, tracking=2)
    bedrooms = fields.Integer(string="Number of Bedrooms", help='Enter the number of bedrooms in the property', default=2)
    living_area = fields.Integer(string="Living Area", help='Enter the living area of the property in square meters')
    facades = fields.Integer(string="Number of Facades", help='Enter the number of facades of the property')
    garage = fields.Boolean(string="Garage", help='Check if the property has a garage')
    garden = fields.Boolean(string="Garden", help='Check if the property has a garden')
    garden_area = fields.Integer(string="Garden Area", help='Enter the area of the garden in square meters')
    garden_orientation = fields.Selection(
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ],
        string="Garden Orientation",
        help='Select the orientation of the garden'
    )
    active = fields.Boolean(string="Active", default=True, help='Set to False to archive the property')
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('canceled', "Canceled")
        ],
        string="Status",
        required=True,
        copy=False,
        default='new',
        store=True,
        readonly=False,
        tracking=1,
        help='Current state of the property'
    )
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    seller_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string="Property Tags", compute="_compute_tags", readonly=False, store=True)

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

    total_area = fields.Integer(string="Total Area", compute="_compute_total_area", help="Total area of the property including living area and garden area", store=True)
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price", help="Best offer received for the property", store=True)
    offer = fields.Float(string="Total Offer", compute="_compute_total_offer", help="This shows the total offers this property has", store=True)
    spam = fields.Boolean(compute="_compute_spam", store=True, default=False)

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price')) if record.offer_ids else 0

    @api.depends("offer_ids")
    def _compute_total_offer(self):
        for record in self:
            record.offer = len(record.mapped('offer_ids'))

    @api.depends("offer_ids.create_date")
    def _compute_spam(self):
        for record in self:
            if record.offer >= 3:
                times = record.offer_ids.filtered('create_date').mapped('create_date')
                partner = record.offer_ids.mapped('partner_id')
                if max(times) - min(times) < timedelta(minutes=5) and len(partner):
                    record.spam = True
            else:
                record.spam = False

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError(_("Canceled properties cannot be sold"))
            record.state = 'sold'

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_("Sold properties cannot be canceled"))
            else:
                record.state = 'canceled'

    def action_reset(self):
        for record in self:
            record.state = 'new'
            record.offer_ids.unlink()

    @api.constrains("selling_price", "expected_price")
    def set_price(self):
        for record in self:
            if record.selling_price > 0 and record.selling_price < record.expected_price * 0.9:
                raise ValidationError("The selling price cannot be lower than 90 percent of the expected price")

    def action_best(self):
        for record in self:
            if not record.offer_ids:
                if len(self) == 1:
                    raise UserError(_("No offers received for this property"))
                else:
                    continue
            for offer in record.offer_ids:
                if offer.price == record.best_price:
                    offer.status = 'accepted'
                    other = record.offer_ids - offer
                    other.status = 'refused'
                    record.buyer_id = offer.partner_id
                    record.selling_price = offer.price
                    if len(self) == 1:
                        return record.action_sold()
                    else:
                        record.action_sold(open_wizard=False)

    @api.depends("expected_price", "state", "offer_ids", "create_date")
    def _compute_tags(self):
        tag_value = self.env['estate.property.tag'].search([])
        high_value = tag_value.filtered(lambda r: r.name == 'High Value')
        if not high_value:
            high_value = self.env['estate.property.tag'].create({'name': 'High Value'})
        low_value = tag_value.filtered(lambda r: r.name == 'Low Interest')
        if not low_value:
            low_value = self.env['estate.property.tag'].create({'name': 'Low Interest'})
        quick_sale = tag_value.filtered(lambda r: r.name == 'Quick sale')
        if not quick_sale:
            quick_sale = self.env['estate.property.tag'].create({'name': 'Quick sale'})
        for record in self:
            if record.expected_price > 50000:
                record.tag_ids |= high_value
            if 0 < len(record.mapped('offer_ids')) < 2:
                record.tag_ids |= low_value
            if record.state == 'sold' and record.create_date:
                deadline = record.create_date.date() + timedelta(days=10)
                if fields.Date.today() <= deadline:
                    record.tag_ids |= quick_sale
                else:
                    record.tag_ids = record.tag_ids

    @api.ondelete(at_uninstall=False)
    def prevent_delete(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise UserError(_("Only new and canceled properties can be deleted"))
