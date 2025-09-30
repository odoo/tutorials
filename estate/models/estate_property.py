from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Properties"
    _order = "id desc"

    @api.ondelete(at_uninstall=False)
    def _unlink_only_new_or_cancelled(self):
        if any(property.state not in ['new', 'cancelled'] for property in self):
            raise UserError(_("Only new and cancelled properties can be deleted."))

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='Status',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        required=True,
        default='new',
        copy=False,
        compute='_compute_state',
        store=True,
    )

    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        "Available from",
        copy=False,
        default=fields.Date.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
    )

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id, required=True)

    total_area = fields.Integer("Total Area (sqm)", compute="_compute_total_area")
    best_price = fields.Float("Best Offer", compute="_compute_best_price")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped('price'), default=0.0)

    @api.depends('offer_ids.status')
    def _compute_state(self):
        for property in self:
            if property.offer_ids:
                accepted_offer = property.offer_ids.filtered(lambda offer: offer.status == 'accepted')
                property.state = 'offer_accepted' if accepted_offer else 'offer_received'
            else:
                property.state = 'new'

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def action_set_sold(self):
        for property in self:
            if property.state == 'cancelled':
                raise UserError(_("Cancelled properties cannot be sold."))
            if not (property.offer_ids and property.offer_ids.filtered(lambda offer: offer.status == 'accepted')):
                raise UserError(_("You cannot sell a property which has no accepted offer."))
            property.state = 'sold'
        return True

    def action_set_cancelled(self):
        for property in self:
            if property.state == 'sold':
                raise UserError(_("Sold properties cannot be cancelled."))
            property.state = 'cancelled'
        return True

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price must be strictly positive.',
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price must be positive.',
    )

    @api.constrains('selling_price', 'expected_price')
    def _check_price_difference(self):
        for property in self:
            if not float_is_zero(property.selling_price, precision_digits=2) and float_compare(property.selling_price, 0.9 * property.expected_price, precision_digits=2) < 0:
                raise UserError(_("The selling price must be at least 90% of the expected price."))
        return True
