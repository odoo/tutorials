from odoo import fields, models, api, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True, string="Partner")
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_id", store=True
    )

    @api.model_create_multi
    def create(self, vals_list):
        offers = super().create(vals_list)
        offers.mapped("property_id").write({"state": "offer_received"})
        return offers

    @api.depends("validity")
    def _compute_date_deadline(self):
        for rec in self:
            if rec.create_date:
                rec.date_deadline = rec.create_date.date() + relativedelta(
                    days=rec.validity
                )
            else:
                rec.date_deadline = fields.Date.today() + relativedelta(
                    days=rec.validity
                )

    def _inverse_date_deadline(self):
        for rec in self:
            if rec.date_deadline and rec.create_date:
                rec.validity = (rec.date_deadline - rec.create_date.date()).days

    def _auto_reject_offer(self):
        rejected_offers = self.search(
            [(("date_deadline", "<", fields.Date.context_today(self)))]
        )
        for offer in rejected_offers:
            offer.status = "refused"

    def action_accept_offer(self):
        estate = self.env["estate.property"].search([("id", "=", self.property_id.id)])
        if any(offer.status == "accepted" for offer in estate.offer_ids):
            raise UserError(_("Only one offer can be accepted at a time."))
        else:
            estate.selling_price = self.price
            estate.buyer_id = self.partner_id.id
            self.status = "accepted"

    def action_refuse_offer(self):
        self.status = "refused"
