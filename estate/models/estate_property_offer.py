from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Esate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price Offered")
    status = fields.Selection(
        copy=False,
        readonly=True,
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
    )
    partner_id = fields.Many2one("res.partner", required=True, string="Buyer")
    property_id = fields.Many2one("estate.property", required=True, string="Property")
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        store=True,
        string="Property Type",
    )
    validity = fields.Integer(default=7, string="Validity")
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True
    )
    _check_offer_price = models.Constraint(
        "CHECK(price > 0)", "The offer price must be strictly positive."
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    @api.model
    def create(self, vals_list):

        for vals in vals_list:
            property_id = vals.get("property_id")

            if property_id:
                property_record = self.env["estate.property"].browse(property_id)
                if property_record.state in ["offer_accepted", "sold", "cancelled"]:
                    raise UserError("Offer for this property cannot be created.")

                existing_offers = property_record.offer_ids
                if existing_offers:
                    max_price = max(existing_offers.mapped("price"))

                    if vals.get("price") <= max_price:
                        raise ValidationError(
                            f"The offer price must be higher than {max_price}."
                        )

        offers = super().create(vals_list)
        for offer in offers:
            if offer.property_id.state == "new":
                offer.property_id.state = "offer_received"

        return offers

    def _inverse_date_deadline(self):
        for record in self:
            create_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.validity = (record.date_deadline - create_date).days

    # def accept_offer(self):
    #     for offer in self:
    #         property_rec = offer.property_id
    #         if property_rec.state in ["sold", "cancelled"]:
    #             raise UserError(
    #                 "you cannot accpet an offer on a solid or cancelled property."
    #             )
    #         remaining_offers = property_rec.offer_ids.filtered(
    #             lambda offer_: offer_.status == "accepted" and offer_ != offer
    #         )
    #         mark_refused = property_rec.offer_ids.filtered(
    #             lambda offer_: offer_.property_id != property_rec
    #         )
    #         breakpoint()
    #         if accepted_offer:
    #             raise UserError("only one offer can be accpeted for a property.")
    #         offer.status = "accepted"

    #         if mark_refused:
    #             offer.status = "refused"

    #         property_rec.write(
    #             {
    #                 "selling_price": offer.price,
    #                 "buyer_id": offer.partner_id.id,
    #                 "state": "offer_accepted",
    #             }
    #         )

    def accept_offer(self):
        for offer in self:
            offer.status = "accepted"
            offer.property_id.write(
                {
                    "selling_price": offer.price,
                    "buyer_id": offer.partner_id.id,
                    "state": "offer_accepted",
                }
            )
            remaining_offers = offer.property_id.offer_ids.filtered(
                lambda offer_: offer_.id != offer.id
            )
            remaining_offers.status = "refused"
            # remaining_offers.write({ 'status' : 'refused'})
            return

    def reject_offer(self):
        for offer in self:
            property_rec = offer.property_id
            if property_rec.state in ["sold", "cancelled"]:
                raise UserError(
                    "you cannot refuse an offer on an sold or cancelled property."
                )
            # if offer.status == "accepted":
            #     other_pending = property_rec.offer_ids.filtered(
            #         lambda offer_: offer_.status == "" and offer_ != offer
            #     )

            #     property_rec.write(
            #         {
            #             "selling_price": 0.0,
            #             "buyer_id": False,
            #             "state": "offer_recieved" if other_pending else "new",
            #         }
            #     )
            #     if other_pending:
            #         property_rec.state = "offer_received"
            #     else:
            #         property_rec.state = "new"
            else:
                offer.status = "refused"
                property_rec.state = "offer_received"
