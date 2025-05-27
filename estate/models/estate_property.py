from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "real estate properties"
    _order = "id desc"

    name = fields.Char('Title', default="Unknown", required=True)
    description = fields.Char('Description')
    postcode = fields.Char('Postcode', required=True, default='00000')

    availability_date = fields.Date('Availability', copy=False, default=lambda: (fields.Date.today() + relativedelta(days=30)))
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2, required=True)
    last_seen = fields.Datetime("Last Seen", default= lambda: fields.Datetime.now)
    expected_price = fields.Float('Expected Price', required=True)
    living_area = fields.Float('Living Area (sqm)')
    facades = fields.Integer('Facades', required=True)
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Float('Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[
            ('north', 'North'),
            ('west', 'West'),
            ('east', 'East'),
            ('south', 'South'),
        ],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='Property State',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        default='new'
    )

    property_type_id = fields.Many2one('estate.property.type', 'Property Type')
    partner_id = fields.Many2one('res.partner', 'Partner')
    seller_id = fields.Many2one('res.users', 'Salesperson', default=lambda self: self.env.user, copy=False)
    tag_ids = fields.Many2many('estate.property.tag', 'property_tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Float('Total Area', compute="_compute_total_area")
    best_offer = fields.Float('Best Offer', compute="_compute_best_offer")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0)', 'A property expected price must be strictly positive!'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'A property selling price must be positive!'),
    ]

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price'))

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 20
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def unlink(self):
        if any(record.state not in ('new', 'cancelled') for record in self):
            raise UserError(_('Only properties in "New" or "Cancelled" state can be deleted.'))
        return super().unlink()

    def action_sell(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_('This property is already taken.'))
            if record.state == 'cancelled':
                raise UserError(_('Property is no longer listed'))
            if record.state != 'offer_accepted':
                raise UserError(_('No offer has been accepted for this property.'))

            record.state = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(_('This Property is already cancelled.'))
            if record.state == 'sold':
                raise UserError(_('Property already sold cannot cancel it.'))

            record.state = 'cancelled'
        return True
