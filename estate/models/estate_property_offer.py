from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "test description 4"
    _order = "price desc"
    _inherit = ["mail.thread", "mail.activity.mixin"]  # enables the chatter

    price = fields.Float(allow_negative=False)
    status = fields.Selection(
        copy=False, selection=[("refused", "Refused"), ("accepted", "Accepted")]
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7, store=True)
    date_deadline = fields.Date(
        compute="_compute_date", inverse="_inverse_date", store=True
    )
    create_date = fields.Date(
        default=lambda self: fields.Datetime.today(), readonly=True, store=True
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )
    fil = fields.Char("DDSDS")

    @api.depends("validity")
    def _compute_date(self):
        for dates in self:
            if dates.validity:
                dates.date_deadline = dates.create_date + relativedelta(
                    days=dates.validity
                )

    def _inverse_date(self):
        for dates in self:
            if dates.date_deadline:
                dates.validity = (dates.date_deadline - dates.create_date).days

    def offer_accept(self):
        if self.property_id.buyer_id:
            raise UserError(
                "This property already has an offer that has been accepted!"
            )
        else:
            if self.price >= (0.9) * self.property_id.expected_price:
                self.property_id.selling_price = self.price
                self.property_id.buyer_id = self.partner_id
                self.status = "accepted"
                self.property_id.state = "offer accepted"
            else:
                raise ValidationError(
                    "The acceptance offer should be atleast 90 percent of the expected price"
                )

    def offer_refuse(self):
        self.status = "refused"
        if self.partner_id == self.property_id.buyer_id:
            self.property_id.buyer_id = None
            self.property_id.selling_price = 0
            self.property_id.state = "offer received"

    @api.constrains("price")
    def _check_price_positive(self):
        for record in self:
            if record.price < 0:
                raise ValidationError("Price cannot be negative!")

    @api.model
    def create(self, vals):
        # Set property state to 'offer received' when creating an offer
        property = self.env["estate.property"].browse(vals.get("property_id"))
        if property:
            if vals["price"] > property.best_price:
                property.state = (
                    "offer received"  # Set the property state when an offer is created
                )
            else:
                raise ValidationError("Bidding Price should be more than best price")
        return super(EstatePropertyOffer, self).create(vals)

    @api.model
    def unlink(self):
        for offer in self:
            # Check if the offer being deleted was the only offer (or the last accepted offer)
            if offer.status == "accepted" and offer.property_id:
                # Look for any other accepted offers for the same property
                remaining_offers = self.env["estate.property.offer"].search(
                    [
                        ("property_id", "=", offer.property_id.id),
                        ("status", "=", "accepted"),
                        ("id", "!=", offer.id),
                    ]
                )

                if not remaining_offers:
                    # If there are no remaining accepted offers, change the property state back to 'new'
                    offer.property_id.state = "new"

        # Call the super method to actually delete the offer
        return super(EstatePropertyOffer, self).unlink()
