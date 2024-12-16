from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import date_utils


class RealEstateProperty(models.Model):
    _name = 'real.estate.property'
    _description = "Real Estate Property"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    image = fields.Image(string="Image")
    state = fields.Selection(
        string="State",
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('under_option', "Under Option"),
            ('sold', "Sold"),
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
    availability_date = fields.Date(string="Availability Date")
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
    address_id = fields.Many2one(string="Address", comodel_name='res.partner', required=True)
    street = fields.Char(string="Street", related='address_id.street', readonly=False, store=True)
    seller_id = fields.Many2one(string="Seller", comodel_name='res.partner', required=True)
    salesperson_id = fields.Many2one(string="Salesperson", comodel_name='res.users')
    offer_ids = fields.One2many(
        string="Offers", comodel_name='real.estate.offer', inverse_name='property_id'
    )
    is_priority = fields.Boolean(
        string="Priority", compute='_compute_is_priority', search='_search_is_priority'
    )
    best_offer_amount = fields.Float(string="Best Offer", compute='_compute_best_offer_amount')
    tag_ids = fields.Many2many(string="Tags", comodel_name='real.estate.tag')
    active = fields.Boolean(string="Active", default=True)

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
