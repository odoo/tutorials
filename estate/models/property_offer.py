import typing

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import date_utils, float_utils

if typing.TYPE_CHECKING:
    from collections.abc import Iterable

    from .property import Property


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offer'
    _order = 'price DESC, id'

    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date(
        'Deadline',
        compute='_compute_deadline',
        inverse='_inverse_deadline',
    )
    property_type_id = fields.Many2one(
        'estate.property.type',
        related='property_id.property_type_id',
    )

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
        for record in self:
            delta_days = (
                record.date_deadline - record.create_date.date()
            ).days if record.date_deadline and record.create_date else 0
            record.validity = delta_days

    @api.model
    def create(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        args: list[dict[str, typing.Any]]
    ) -> typing.Any:
        for record in args:
            property_id: int = record['property_id']
            property = typing.cast(
                'Property',
                self.env['estate.property'].browse(property_id)
            )
            property.ensure_one()

            for offer in typing.cast(
                'Iterable[PropertyOffer]',
                property.offer_ids,
            ):
                if float_utils.float_compare(
                    record['price'],
                    offer.price,
                    precision_rounding=.01,
                ) == -1:
                    raise UserError(
                        "Can't create an offer with a lower amount than an "
                        'existing offer.'
                    )

            if property.state == 'new':
                property.state = 'offer_received'

        return super().create(args)

    @api.ondelete(at_uninstall=False)
    def _unlink_and_reset_property_state(self) -> None:
        for record in self:
            property = typing.cast('Property', record.property_id)
            if (
                property.state == 'offer_received'
                and len(property.offer_ids) == 1
                and property.offer_ids[0].id == record.id
            ):
                property.state = 'new'

    def action_accept(self) -> bool:
        for record in self:
            property = typing.cast('Property', record.property_id)
            offers = typing.cast('Iterable[PropertyOffer]', property.offer_ids)

            if any(
                offer.status == 'accepted'
                for offer in offers
            ):
                raise UserError(
                    'An offer is already accepted for this property.'
                )

            record.status = 'accepted'
            property.selling_price = record.price
            property.buyer_id = record.partner_id
            property.state = 'offer_accepted'

        return True

    def action_refuse(self) -> bool:
        for record in self:
            property = typing.cast('Property', record.property_id)
            record.status = 'refused'
            property.selling_price = property.expected_price
            property.buyer_id = False

        return True
