from odoo import models, fields, api
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate_property_offer"
    _description = "this is defind the offer of properties"

    price = fields.Float("offer_price")
    status = fields.Selection(
        [("Accepted", "accepted"), ("Refused", "refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate_property", required=True)

    validity = fields.Integer("Offer Validity", default=7)
    date_deadline = fields.Date(
        "Deadline", compute="_compute_deadline", inverse="_compute_validity"
    )

    _check_offer_price_positive=models.Constraint('CHECK(price>0)',"The offer price must be strictly positive")

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(
                record.create_date or fields.Date.today(), days=record.validity
            )


    def _compute_validity(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days


    def action_accept_offer(self):
        for record in self:
            if (record.property_id.state=="Offer Accepted"):
                raise UserError(message="one offer is already accpted")

            else:
                record.status="Accepted"
                record.property_id.selling_price=record.price
                record.property_id.buyer_id=record.partner_id
                record.property_id.state="Offer Accepted"

        return True
            

    def action_refused_offer(self):
        for record in self:
            record.status="Refused"

        return True


    