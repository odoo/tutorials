from odoo import api, fields, models
from datetime import timedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date("Deadline", compute="_compute_date_deadline")
    hide_offer_buttons = fields.Boolean(compute="_compute_hide_offer_buttons")
    property_type_id = fields.Many2one(related="property_id.type_id", store=True)
    _check_price = models.Constraint(
        "CHECK(price > 0)", "Offer's price must be positive"
    )
    _order = "price desc"

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (
                record.create_date or fields.Datetime.now()
            ) + timedelta(days=record.validity)

    @api.depends("property_id.state")
    def _compute_hide_offer_buttons(self):
        for record in self:
            a_state = record.property_id.state
            if (
                a_state == "offer_accepted"
                or a_state == "cancelled"
                or a_state == "sold"
                or record.status
            ):
                record.hide_offer_buttons = True
            else:
                record.hide_offer_buttons = False

    def action_accept_offer(self):
        if self.status:
            raise UserError("You cannot change the status!")
        if self.property_id.state == "offer_accepted":
            raise UserError("One offer has been already accepted, sorry!")
        if self.property_id.state == "cancelled":
            raise UserError("This property is cancelled")
        if self.property_id.state == "sold":
            raise UserError("This property is sold")

        for record in self:
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "offer_accepted"
        return True

    def action_refuse_offer(self):
        if self.status:
            raise UserError("You cannot change the status!")
        for record in self:
            record.status = "refused"
        return True

    def is_still_open_to_offers(self):
        if (
            self.partner_id.state == "offer_accepted"
            or self.partner_id.state == "sold"
            or self.partner_id.state == "cancelled"
        ):
            print("HELLO!!")
            return True

        print("FALSE case!!")
        return False

    # @api.depends("create_date", "date_deadline") Not working right now!!!
    # def _inverse_date_deadline(self):
    #     print("Hello!")
    #     for record in self:
    #         record.validity = (
    #             (record.date_deadline or fields.Datetime.now())
    #             - (record.create_date or fields.Datetime.now())
    #         ).days
