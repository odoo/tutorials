from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare

from .estate_property import CLOSED_STATES


class EstatePropertyOffer(models.Model):
    """An amount offered by a potential buyer for a property."""

    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        string="Status",
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    # An offer has no meaning without its property: delete it with the property.
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
        ondelete="cascade",
    )
    # Stored so that the offers can be searched by property type (stat button
    # on the property types).
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        related="property_id.property_type_id",
        store=True,
    )
    # The validity and the deadline can both be edited: each one updates the
    # other (see the compute and inverse methods).
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be strictly positive.',
    )
    _check_validity = models.Constraint(
        'CHECK(validity > 0)',
        'The validity of an offer must be strictly positive.',
    )

    @api.depends("partner_id", "price")
    def _compute_display_name(self):
        """Offers have no name field: display them as "<partner> - <price>"."""
        for offer in self:
            offer.display_name = self.env._(
                "%(partner)s - %(price).2f",
                partner=offer.partner_id.display_name,
                price=offer.price,
            )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = fields.Date.add(offer._get_start_date(), days=offer.validity)

    def _inverse_date_deadline(self):
        """Update the validity when the user sets the deadline directly."""
        for offer in self:
            offer.validity = (offer.date_deadline - offer._get_start_date()).days

    @api.model_create_multi
    def create(self, vals_list):
        """Create the offers, then check them against their property.

        The checks are done on the created records rather than on vals_list,
        so that they also apply when the property is not in the values (e.g.
        given by default_property_id in the context).
        """
        offers = super().create(vals_list)
        offers._ensure_new_offers_valid()
        return offers

    @api.ondelete(at_uninstall=False)
    def _unlink_except_accepted(self):
        """The buyer and selling price of the property come from the accepted offer."""
        if "accepted" in self.mapped("status"):
            raise UserError(self.env._(
                "Accepted offers cannot be deleted: the buyer and the selling "
                "price of the property depend on them."
            ))

    def action_accept(self):
        """Accept the offers and set the buyer and selling price of their property.

        All the checks are done before writing. The state of the property
        becomes "Offer Accepted" through its computation.
        """
        self._ensure_properties_open()
        if self.filtered(lambda offer: offer.date_deadline < fields.Date.today()):
            raise UserError(self.env._("Expired offers cannot be accepted."))
        # self.property_id has no duplicates: fewer properties than offers
        # means that several offers of the same property are being accepted.
        if len(self.property_id) < len(self):
            raise UserError(self.env._("Only one offer can be accepted per property."))
        if "accepted" in self.property_id.offer_ids.mapped("status"):
            raise UserError(self.env._(
                "An offer has already been accepted for this property."
            ))
        self.write({"status": "accepted"})
        # Each property gets its own values: one write per property.
        for offer in self:
            offer.property_id.write({
                "selling_price": offer.price,
                "buyer_id": offer.partner_id.id,
            })
        return True

    def action_refuse(self):
        self._ensure_properties_open()
        self.write({"status": "refused"})
        return True

    def _ensure_new_offers_valid(self):
        """Raise if the newly created offers in self cannot be made.

        No offer can be made once an offer has been accepted, nor on a closed
        property, and each offer must be higher than all the previous offers
        of its property, including the ones created in the same batch.
        """
        for estate_property in self.property_id:
            # The state is already recomputed with the new offers: it is still
            # "Offer Accepted" if another offer had been accepted before.
            if estate_property.state in ("offer_accepted", *CLOSED_STATES):
                raise UserError(self.env._(
                    "New offers cannot be made once an offer has been accepted, "
                    "or on sold or cancelled properties."
                ))
            new_offers = self.filtered(lambda offer: offer.property_id == estate_property)
            best_price = max((estate_property.offer_ids - new_offers).mapped("price"), default=0.0)
            # Check the new offers in their creation order, each one raising
            # the price that the next ones must reach.
            for offer in new_offers:
                if float_compare(offer.price, best_price, precision_digits=2) < 0:
                    raise UserError(self.env._(
                        "The offer must be higher than %s.", best_price
                    ))
                best_price = offer.price

    def _ensure_properties_open(self):
        """Offers of sold or cancelled properties are kept as history."""
        if any(state in CLOSED_STATES for state in self.property_id.mapped("state")):
            raise UserError(self.env._(
                "Offers of sold or cancelled properties cannot be changed."
            ))

    def _get_start_date(self):
        """Return the date from which the validity is counted.

        The creation date is only set once the offer is saved, so today's
        date is used as a fallback for offers being created.
        """
        self.ensure_one()
        return self.create_date.date() if self.create_date else fields.Date.today()
