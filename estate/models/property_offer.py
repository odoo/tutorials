import typing

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import date_utils, format_list

from . import rel

if typing.TYPE_CHECKING:
    from odoo.addons.base.models.res_company import ResCompany
    from odoo.addons.base.models.res_currency import ResCurrency

    from .property import Property


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offer'
    _order = 'price DESC, id'

    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        selection=[  # pyright: ignore[reportArgumentType]
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id: fields.Field['Property'] = rel(
        fields.Many2one('estate.property', required=True, ondelete='cascade')
    )
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date(
        'Deadline',
        compute='_compute_deadline',
        inverse='_inverse_deadline',
    )
    property_type_id = fields.Many2one(related='property_id.property_type_id')

    create_date: fields.Datetime  # From Model

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The price of an offer must be strictly positive.',
    )

    @api.depends('validity')
    def _compute_deadline(self) -> None:
        today = fields.Date.today()

        for record in self:
            create_date = record.create_date or today
            record.date_deadline = date_utils.add(
                create_date,
                days=record.validity,
            )

    def _inverse_deadline(self) -> None:
        today = fields.Datetime.today()

        for record in self:
            create_date = record.create_date or today
            delta_days = (
                record.date_deadline - create_date.date()
            ).days if record.date_deadline else 0
            record.validity = delta_days

    @api.depends(
        'property_id.display_name',
        'partner_id.display_name',
        'price',
    )
    @api.depends_context('company', 'lang')
    def _compute_display_name(self) -> None:
        company = typing.cast('ResCompany', self.env.company)
        currency = typing.cast('ResCurrency', company.currency_id)

        for record in self:
            record.display_name = self.env._(
                'Offer for %(property)s '
                'from %(partner)s '
                'for %(amount)s',
                property=record.property_id.display_name,
                partner=(
                    record.partner_id.display_name
                    or self.env._('Unknown buyer')
                ),
                amount=currency.format(record.price),
            )

    @api.model_create_multi
    def create(self, vals_list: list[dict[str, typing.Any]]) -> typing.Any:
        properties = typing.cast(
            'Property',
            self.env['estate.property']
        ).browse(
            vals['property_id']
            for vals in vals_list
        )

        if unavailable := properties.filtered(
            lambda property: not property.available
        ):
            raise UserError(self.env._(
                'Cannot create offers on properties %(properties)s: '
                'properties are not available.',
                properties=unavailable._quoted_names(),
            ))

        properties_by_id = {
            property.id: property
            for property in properties
        }
        company = typing.cast('ResCompany', self.env.company)
        currency = typing.cast('ResCurrency', company.currency_id)

        for vals in vals_list:
            property = properties_by_id[vals['property_id']]

            if property.best_offer_id and currency.compare_amounts(
                vals['price'],
                property.best_price,
            ) < 0:
                raise UserError(self.env._(
                    'Cannot create an offer for %(offer_price)s, it is lower '
                    'than %(best_offer)s.',
                    offer_price=currency.format(vals['price']),
                    best_offer=property.best_offer_id.display_name,
                ))

        properties.filtered(
            lambda property: property.state == 'new'
        ).state = 'offer_received'

        return super().create(vals_list)

    @api.ondelete(at_uninstall=False)
    def _unlink_except_accepted_or_closed(self) -> None:
        if offers := self.filtered(lambda offer: offer.status == 'accepted'):
            raise UserError(self.env._(
                'Cannot delete accepted offers: %(offers)s.',
                offers=format_list(self.env, offers.mapped('display_name'))
            ))

        if properties := self.property_id.filtered('closed'):
            raise UserError(self.env._(
                'Cannot delete offers on properties %(properties)s: '
                'properties are sold or cancelled.',
                properties=properties._quoted_names(),
            ))

        self.property_id.filtered(lambda property: (
            property.state == 'offer_received'
            and not (property.offer_ids - self)
        )).state = 'new'

    def action_accept(self) -> bool:
        if offers := self.filtered(lambda offer: offer.status == 'refused'):
            raise UserError(self.env._(
                'Cannot accept refused offers %(offers)s. Create a new offer '
                'instead.',
                offers=format_list(self.env, offers.mapped('display_name')),
            ))

        if properties := self.property_id.filtered(
            lambda property: property.state == 'offer_accepted'
        ):
            raise UserError(self.env._(
                'Cannot accept offers on properties %(properties)s: an offer '
                'is already accepted for these properties.',
                properties=properties._quoted_names(),
            ))

        if properties := self.property_id.filtered('closed'):
            raise UserError(self.env._(
                'Cannot accept offers on properties %(properties)s: '
                'properties are already sold or cancelled.',
                properties=properties._quoted_names(),
            ))

        offers_by_property = self.grouped(lambda offer: offer.property_id)
        if offers := self.browse().concat(
            offers
            for offers in offers_by_property.values()
            if len(offers) > 1
        ):
            raise UserError(self.env._(
                'Cannot accept conflicting offers %(offers)s on properties '
                '%(properties)s.',
                offers=format_list(self.env, offers.mapped('display_name')),
                properties=offers.property_id._quoted_names(),
            ))

        for record in self:
            property = record.property_id
            property.selling_price = record.price
            property.buyer_id = record.partner_id
            property.state = 'offer_accepted'

        self.status = 'accepted'

        return True

    def action_refuse(self) -> bool:
        if properties := self.property_id.filtered('closed'):
            raise UserError(self.env._(
                'Cannot refuse offers on properties %(properties)s: '
                'properties are sold or cancelled.',
                properties=properties._quoted_names(),
            ))

        for record in self.filtered(lambda offer: offer.status == 'accepted'):
            property = record.property_id
            property.selling_price = 0
            property.buyer_id = False
            property.state = 'offer_received'

        self.status = 'refused'

        return True
