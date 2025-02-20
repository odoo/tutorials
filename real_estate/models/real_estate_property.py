from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import date_utils


class RealEstateProperty(models.Model):
    _name = 'real.estate.property'
    _description = "Real Estate Property"
    _sql_constraints = [(
        'positive_price',
        'CHECK (selling_price > 0)',
        "The selling price must be strictly positive.",
    )]

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    image = fields.Image(string="Image")
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('under_option', "Under Option"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        required=True,
        default='new',
    )
    type_id = fields.Many2one(
        string="Type", comodel_name='real.estate.property.type', ondelete='restrict', required=True
    )
    selling_price = fields.Float(
        string="Selling Price", help="The selling price excluding taxes.", required=True
    )
    availability_date = fields.Date(
        string="Availability Date",
        default=lambda self: date_utils.add(fields.Date.today(), months=2)
    )
    stalled = fields.Boolean(string="Stalled", compute='_compute_stalled', search='_search_stalled')
    floor_area = fields.Integer(
        string="Floor Area", help="The floor area in square meters excluding the garden."
    )
    bedrooms = fields.Integer(string="Number of Bedrooms", default=2)
    has_garage = fields.Boolean(string="Garage")
    has_garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(
        string="Garden Area", help="The garden area excluding the building."
    )
    total_area = fields.Integer(string="Total Area", compute='_compute_total_area', store=True)
    address_id = fields.Many2one(string="Address", comodel_name='res.partner')
    street = fields.Char(string="Street", related='address_id.street', readonly=False, store=True)
    seller_id = fields.Many2one(string="Seller", comodel_name='res.partner', required=True)
    salesperson_id = fields.Many2one(
        string="Salesperson", comodel_name='res.users', default=lambda self: self.env.user
    )
    offer_ids = fields.One2many(
        string="Offers", comodel_name='real.estate.offer', inverse_name='property_id'
    )
    offer_count = fields.Integer(string="Offer Count", compute='_compute_offer_count')
    is_priority = fields.Boolean(
        string="Priority", compute='_compute_is_priority', search='_search_is_priority'
    )
    best_offer_amount = fields.Float(string="Best Offer", compute='_compute_best_offer_amount')
    tag_ids = fields.Many2many(string="Tags", comodel_name='real.estate.tag')

    @api.depends('availability_date')
    def _compute_stalled(self):
        for property in self:
            property.stalled = property.availability_date < fields.Date.today()

    def _search_stalled(self, operator, value):
        if (operator == '=' and value is True) or (operator == '!=' and value is False):
            return [('availability_date', '<', fields.Date.today())]
        elif (operator == '=' and value is False) or (operator == '!=' and value is True):
            return [('availability_date', '>=', fields.Date.today())]
        else:
            raise NotImplementedError()

    @api.depends('floor_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.floor_area + property.garden_area

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        offer_data = self.env['real.estate.offer']._read_group(
            [('property_id', 'in', self.ids)], groupby=['property_id'], aggregates=['__count'],
        )
        property_data = {property.id: count for property, count in offer_data}
        for property in self:
            property.offer_count = property_data.get(property.id, 0)

    @api.depends('offer_ids.expiry_date')
    def _compute_is_priority(self):
        for property in self:
            is_priority = False
            for offer in property.offer_ids:
                if offer.expiry_date <= fields.Date.today() + date_utils.relativedelta(days=2):
                    is_priority = True
                    break
            property.is_priority = is_priority

    def _search_is_priority(self, operator, value):
        if (operator == '=' and value is True) or (operator == '!=' and value is False):
            return [(
                'offer_ids.expiry_date',
                '<=',
                fields.Date.today() + date_utils.relativedelta(days=2),
            )]
        elif (operator == '=' and value is False) or (operator == '!=' and value is True):
            return [(
                'offer_ids.expiry_date',
                '>',
                fields.Date.today() + date_utils.relativedelta(days=2),
            )]
        else:
            raise NotImplementedError()

    @api.depends('offer_ids.amount')
    def _compute_best_offer_amount(self):
        for property in self:
            if property.offer_ids:
                property.best_offer_amount = max(property.offer_ids.mapped('amount'))
            else:
                property.best_offer_amount = 0

    @api.constrains('availability_date')
    def _check_availability_date_under_1_year(self):
        for property in self.filtered('availability_date'):
            if property.availability_date > fields.Date.today() + date_utils.relativedelta(years=1):
                raise ValidationError(_("The availability date must be in less than one year."))

    @api.onchange('active')
    def _onchange_active_block_if_existing_offers(self):
        if not self.active:
            existing_offers = self.env['real.estate.offer'].search(
                [('property_id', '=', self._origin.id), ('state', '=', 'waiting')]
            )
            if existing_offers:
                raise UserError(
                    _("You cannot change the active state of a property that has pending offers.")
                )

    @api.onchange('has_garden')
    def _onchange_has_garden_set_garden_area_to_zero_if_unchecked(self):
        if not self.has_garden:
            self.garden_area = 0

    @api.onchange('garden_area')
    def _onchange_garden_area_uncheck_garden_if_zero(self):
        if self.garden_area and not self.has_garden:
            self.has_garden = True

    @api.onchange('garden_area')
    def _onchange_garden_area_display_warning_if_zero_and_checked(self):
        if not self.garden_area and self.has_garden:
            return {
                'warning': {
                    'title': _("Warning"),
                    'message': _(
                        "The garden area was set to zero, but the garden checkbox is checked."
                    ),
                }
            }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('address_id'):  # No address is provided at creation time.
                # Create and assign a new one based on the property name.
                address = self.env['res.partner'].create({
                    'name': vals.get('name'),
                })
                vals['address_id'] = address.id
        return super().create(vals_list)

    def write(self, vals):
        res = super().write(vals)
        if vals.get('street'):  # The street has been updated.
            for property in self:
                if not property.address_id:  # The property has no address record.
                    # Create and assign a new one based on the property name and the street.
                    address = self.env['res.partner'].create({
                        'name': property.name,
                        'street': vals['street'],
                    })
                    property.address_id = address.id
        return res

    def action_cancel_listing(self):
        for property in self:
            property.offer_ids.action_refuse()
            property.write({
                'state': 'cancelled',
                'active': False,
            })
        return True

    def action_assign_user_as_salesperson(self):
        self.salesperson_id = self.env.user.id
        return True
