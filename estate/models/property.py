import typing

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import date_utils, format_list

from . import rel

if typing.TYPE_CHECKING:
    from odoo.addons.base.models.res_company import ResCompany
    from odoo.addons.base.models.res_currency import ResCurrency

    from .property_offer import PropertyOffer


class Property(models.Model):
    _name = 'estate.property'
    _description = 'Property'
    _order = 'id DESC'

    name = fields.Char('Title', required=True, translate=True)
    description = fields.Text('Description', translate=True)
    postcode = fields.Char('Postcode')
    date_availability = fields.Date(
        'Available From',
        copy=False,
        default=lambda _: date_utils.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[  # pyright: ignore[reportArgumentType]
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
    )
    state = fields.Selection(
        string='Status',
        selection=[  # pyright: ignore[reportArgumentType]
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        required=True,
        copy=False,
        default='new',
    )
    active = fields.Boolean('Active', default=True)
    property_type_id = fields.Many2one(
        'estate.property.type',
        string='Property Type',
    )
    buyer_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        readonly=True,
        copy=False,
    )
    salesperson_id = fields.Many2one(
        'res.users',
        string='Salesman',
        default=lambda self: self.env.user,
    )
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids: fields.Field['PropertyOffer'] = rel(fields.One2many(
        'estate.property.offer',
        'property_id',
        string='Offers',
    ))
    total_area = fields.Integer(
        'Total Area (sqm)',
        compute='_compute_total_area',
    )
    best_offer_id: fields.Field['PropertyOffer'] = rel(fields.Many2one(
        'estate.property.offer',
        string='Best Offer',
        compute='_compute_best_offer_id',
        store=True,
    ))
    best_price = fields.Float(
        'Best Offer Price',
        related='best_offer_id.price',
        store=True,
    )
    closed = fields.Boolean(
        'Closed',
        compute='_compute_closed',
    )
    available = fields.Boolean(
        'Available',
        compute='_compute_available',
        store=True,
    )

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price of a property must be strictly positive.',
    )
    _check_selling_price_positive = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price of a property must be positive.',
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self) -> None:
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price', 'offer_ids.status')
    def _compute_best_offer_id(self) -> None:
        for record in self:
            record.best_offer_id = max(
                record.offer_ids.filtered(
                    lambda offer: offer.status != 'refused'
                ),
                key=lambda offer: offer.price,
                default=False,
            )

    @api.depends('state')
    def _compute_closed(self) -> None:
        for record in self:
            record.closed = record.state in {'sold', 'cancelled'}

    @api.depends('state')
    def _compute_available(self) -> None:
        for record in self:
            record.available = record.state in {'new', 'offer_received'}

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_against_expected_price(self) -> None:
        company = typing.cast('ResCompany', self.env.company)
        currency = typing.cast('ResCurrency', company.currency_id)

        if properties := self.filtered(
            lambda property: (
                not currency.is_zero(property.selling_price)
                and currency.compare_amounts(
                    property.selling_price,
                    property.expected_price * .90,
                ) < 0
            )
        ):
            raise ValidationError(self.env._(
                'The selling price must be at least 90%% of the expected '
                'price on %(properties)s.',
                properties=properties._quoted_names(),
            ))

    @api.onchange('garden')
    def _onchange_garden(self) -> None:
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _unlink_if_property_new_or_cancelled(self) -> None:
        if properties := self.filtered(
            lambda property: property.state not in {'new', 'cancelled'}
        ):
            raise UserError(self.env._(
                'Cannot delete properties %(properties)s: only new and '
                'cancelled properties can be deleted.',
                properties=properties._quoted_names(),
            ))

    def action_sold(self) -> bool:
        if properties := self.filtered('closed'):
            raise UserError(self.env._(
                'Cannot sell properties %(properties)s: properties are '
                'already sold or cancelled.',
                properties=properties._quoted_names(),
            ))

        if properties := self.filtered(
            lambda property: property.state != 'offer_accepted'
        ):
            raise UserError(self.env._(
                'Cannot sell properties %(properties)s: properties have no '
                'accepted offer.',
                properties=properties._quoted_names(),
            ))

        self.offer_ids.filtered(
            lambda offer: offer.status != 'accepted'
        ).action_refuse()
        self.state = 'sold'

        return True

    def action_cancel(self) -> bool:
        if properties := self.filtered('closed'):
            raise UserError(self.env._(
                'Cannot cancel properties %(properties)s: properties are '
                'already sold or cancelled.',
                properties=properties._quoted_names(),
            ))

        self.offer_ids.filtered(
            lambda offer: offer.status != 'refused'
        ).action_refuse()
        self.state = 'cancelled'

        return True

    def _quoted_names(self) -> str:
        names: str = format_list(
            self.env,
            self.mapped(lambda property: f'"{property.display_name}"')
        )
        return names
