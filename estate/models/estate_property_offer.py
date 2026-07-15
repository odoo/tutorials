from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"


    price = fields.Float()
    validity = fields.Integer(
        default=7,
    )
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one(
        "res.partner",
        required=True,
    )
    property_id = fields.Many2one(
        "estate.property",
        required=True,
    )
    # STAT BUTTON
    property_type_id = fields.Many2one(
        "estate.property.type",
        # Offer--property_id--Property--property_type_id--Property Type
        related="property_id.property_type_id",
        store=True,
    )

    # SQL Constraints
    # Offer price must be strictly positive
    _check_offer_price = models.Constraint(
        'CHECK(price > 0)',
        'Offer Price must be strictly positive.',
    )

    # Compute deadline date
    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            # Will use the offer's creation date if it exists.
            # When creating a new offer, create_date is still false/empty because the record hasn't been saved yet
            # So, if create_date exists, use it else use today's date temporarly
            create_date = (
                offer.create_date.date()
                if offer.create_date
                else fields.Date.today()
            )
            # Calculating deadline by adding the validity period (no.of days) to the creation date.
            offer.date_deadline = (
                create_date +
                timedelta(days=offer.validity)
            )

    # Inverse date deadline
    def _inverse_date_deadline(self):
        for offer in self:
            # Use the creation date if available, otherwise, use today's date for new records.
            create_date = (
                offer.create_date.date()
                if offer.create_date
                else fields.Date.today()
            )
            # Only calculate validity if a deadline has been set.
            if offer.date_deadline:
                # Validity = deadline - creation date
                offer.validity = (
                    offer.date_deadline -
                    create_date
                ).days

    # Accept the offer
    def action_accept(self):
        for offer in self:
            # Check if another offer for this property has already been accpted
            if offer.property_id.offer_ids.filtered(
                lambda o: o.status == "accepted" and o.id != offer.id
            ):
                raise UserError(
                    "Another offer for this property has already been accepted."
                )
            # Set the status to "accepted"
            offer.status = "accepted"
            # Updating the related property fields
            offer.property_id.write({
                "buyer_id": offer.partner_id.id,
                "selling_price": offer.price,
                "state": "offer_accepted",
            })
        return True

    # def action_accept(self):
    #     for offer in self:
    #         # Check every offer of the same property
    #         for other_offer in offer.property_id.offer_ids:
    #             # Ignore the current offer and check if another offer is accepted
    #             if (
    #                 other_offer.status == "accepted"
    #                 and other_offer.id != offer.id
    #             ):
    #                 raise UserError(
    #                     "Another offer for this property has already been accepted."
    #                 )
    #         # Accept the current offer
    #         offer.status = "accepted"
    #         # Update the property
    #         offer.property_id.write({
    #             "buyer_id": offer.partner_id.id,
    #             "selling_price": offer.price,
    #             "state": "offer_accepted",
    #         })
    #     return True

    # Refuse the offer and set the status to "refused"
    def action_refuse(self):
        for offer in self:
            offer.status = "refused"
        return True

    # Whenever a new offer is created for a property, if the property is still in the new state, automatically change its state to offer_received.
    @api.model_create_multi
    def create(self, vals_list):
        offers = super().create(vals_list)
        for offer in offers:
            if offer.property_id.state == "new":
                offer.property_id.state = "offer_received"
        return offers

    # # Overriding the create() method to execute custom logic whenever new offers are created.
    # @api.model_create_multi
    # def create(self, vals_list):
    #     # Before calling super record doesn't exist, so it creates records in DB and return them as recordset
    #     offers = super().create(vals_list)
    #     for offer in offers:
    #         # If the property is still marked as "new", means this is the first offer received.
    #         if offer.property_id.state == "new":
    #             # Update the property's state to "offer_received" to indicate that at least one offer now exists.
    #             offer.property_id.state = "offer_received"
    #     return offers
