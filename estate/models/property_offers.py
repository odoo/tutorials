from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import timedelta


class PropertyOffers(models.Model):
    _name = "property.offers"
    _description = "Property Offers"

    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )

    # relationships
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    # inverse function fields
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    # compute deadline date using (validity days)
    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            # need a fallback to prevent crashing at time of creation.
            create_date = record.create_date or fields.Datetime.now()
            record.date_deadline = create_date + timedelta(days=record.validity)

    # compute validity (days) using deadline date with inverse function
    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (
                    record.date_deadline - record.create_date.date()
                ).days
            else:
                record.validity = 7

    # action method when offer is accepted (accept button is clicked)
    def action_accept(self):
        for offer in self:
            if offer.status == "accepted":
                raise UserError("This offer is already accepted.")

            offer.status = "accepted"

            # set other offers status to refused
            for other_offer in offer.property_id.offer_ids:
                if other_offer.id != offer.id:
                    other_offer.status = "refused"

            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
        return True

    # action method when offer is refused
    def action_refuse(self):
        self.status = "refused"
        return True

    # sql constraints
    _sql_constraints = [
        ("price", "CHECK(price >= 0)", "Price must be strictly positive")
    ]
