from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class PropertyOffers(models.Model):
    _name = "property.offers"
    _description = "Property Offers"
    _order = "price desc"

    # sql constraints
    _sql_constraints = [
        ("price", "CHECK(price >= 0)", "Price must be strictly positive")
    ]

    # Fields
    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )

    # inverse function fields
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    # relationships
    partner_id = fields.Many2one(
        string="Partner", comodel_name="res.partner", required=True
    )
    property_id = fields.Many2one(
        string="Property", comodel_name="estate.property", required=True
    )
    property_type_id = fields.Many2one(
        string="Property Type", related="property_id.property_type_id", store=True
    )

    # compute deadline date using (validity days)
    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
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

    # set state to offer_received when an offer is created
    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            property_id = val.get("property_id")
            if property_id:
                property_obj = self.env["estate.property"].browse(property_id)
                is_offer_exists = self.env["property.offers"].search(
                    [
                        ("property_id", "=", property_obj.id),
                        ("price", ">", val.get("price")),
                    ],
                    limit=1,
                )

                if is_offer_exists:
                    raise UserError(
                        "The offer price cannot be lower than an existing offer."
                    )
                property_obj.state = "offer_received"

        return super(PropertyOffers, self).create(vals)

    # action method when offer is accepted (accept button is clicked)
    def action_accept(self):
        for offer in self:
            if offer.status == "accepted":
                raise UserError("This offer is already accepted.")

            offer.status = "accepted"

            for other_offer in offer.property_id.offer_ids:
                if other_offer.id != offer.id:
                    other_offer.status = "refused"

            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.state = "offer_accepted"
        return True

    # action method when offer is refused
    def action_refuse(self):
        self.status = "refused"
        return True
