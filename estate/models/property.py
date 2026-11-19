from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import date_utils, float_utils as fu


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property type"

    name = fields.Char('Name', required=True)

    _name_uniq = models.Constraint(
        'unique(name)',
        'A property type with the same name already exists.',
    )


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate property"

    name = fields.Char('Property Name', required=True)
    description = fields.Text('Property Description')
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='Current Status',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        default='new',
        required=True
    )
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Availability Date', default=lambda self: date_utils.add(fields.Datetime.today(), months=3), copy=False)
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', help="Number of bedrooms", default=2)
    living_area = fields.Integer('Living Area (m²)')
    facades = fields.Integer('Facades', help="Number of facades")
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (m²)')
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Indicates the orientation of the garden"
    )

    type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

    total_area = fields.Integer('Total Area (m²)', compute="_compute_total_area")
    best_offer = fields.Float('Best Offer', compute="_compute_best_offer")

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price must be strictly positive'
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price > 0)',
        'The selling price must be strictly positive'
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            best_offer = 0.0 if not record.best_offer else record.best_offer
            for offer in record.offer_ids:
                record.best_offer = max(best_offer, offer.price)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = self.garden_area if self.garden_area else 10
            self.garden_orientation = self.garden_orientation if self.garden_orientation else 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    @api.constrains("selling_price", "expected_price")
    def check_selling_price(self):
        for record in self:
            if not fu.float_is_zero(record.selling_price, precision_digits=2) and fu.float_compare(record.selling_price, (record.expected_price * 0.9), precision_rounding=0.01) < 0:
                raise ValidationError(_('The selling price must be at least 90%% of the expected_price : \n The accepted Selling Price (%s) is %s %% of the expected price (%s)') % (record.selling_price, fu.float_round((record.selling_price / record.expected_price) * 100, 2), record.expected_price))

    @api.depends("selling_price", "offer_ids", "buyer_id")
    def accept_offer(self, offer_id):
        for record in self:
            for offer in record.offer_ids:
                if offer.id == offer_id:
                    record.selling_price = offer.price
                    record.buyer_id = offer.buyer_id
                else:
                    offer.state = 'refused'

    @api.constrains("offer_ids")
    def check_offer_ids(self):
        for record in self:
            accepted = 0
            for offer in record.offer_ids:
                if offer.state == 'accepted':
                    accepted +=1
                if accepted > 1:
                    raise ValidationError('Only one offer can be accepted, refuse the previous accepted offer before accepted another one.')

    @api.onchange("offer_ids")
    @api.depends("selling_price", "buyer_id")
    def _onchange_offer_ids(self):
        for record in self:
            for offer in record.offer_ids:
                if offer.state == 'accepted':
                    record.selling_price = offer.price
                    record.buyer_id = offer.buyer_id

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError('Canceled property cannot be sold')
            else:
                record.state = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('Sold property cannot be canceled')
            else:
                record.state = 'cancelled'
        return True
