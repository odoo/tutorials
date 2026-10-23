from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offers"
    _order = 'price desc'

    name = fields.Char()
    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    _check_offer_price = models.Constraint("CHECK (price > 0)", "Offer price must be stricly positive")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            creation_date = (record.create_date or fields.Datetime.today()).date()
            record.date_deadline = fields.Date.add(creation_date, days=record.validity)

    @api.model_create_multi
    def create(self, offers_list):
        for offer in offers_list:
            record = self.env["estate.property"].browse(offer["property_id"])

            current_offer = record.offer_ids.mapped("price")
            if current_offer and float_compare(offer.get("price", 0.0), max(current_offer), precision_digits=2) < 0:
                raise UserError(f"The offer must be higher than {max(current_offer)}")

            if record.state == "new":
                record.state = "offer_received"

        return super().create(offers_list)

    def _inverse_date_deadline(self):
        for record in self:
            if (record.date_deadline):
                creation_date = (record.create_date or fields.Datetime.today()).date()
                record.validity = (record.date_deadline - creation_date).days

    def action_offer_accept(self):
        for record in self:
            if "accepted" in record.property_id.offer_ids.mapped("status"):
                raise UserError("An offer has already been accepted.")
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "offer_accepted"
        return True

    def action_offer_refuse(self):
        for record in self:
            record.status = "refused"
        return True
