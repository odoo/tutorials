"""module for the estate property offer model"""

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models

class EstatePropertyOffer(models.Model):
    "Estate property type odoo model"
    _name = "estate.property.offer"
    _description= "real estate offers"
    _order="price desc"

    price = fields.Float("Price")
    status = fields.Selection(
            [("accepted", "Accepted"), ("refused", "Refused")],
            string = "Status",
            copy = False)
    partner_id = fields.Many2one('res.partner', required = True, string = "Prospective Buyer")
    property_id = fields.Many2one('estate.property', required = True, string = "Property", ondelete='cascade')
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date("Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(related = "property_id.type_id")

    def action_accept(self):
        self.ensure_one()

        property = self.property_id
        property.state = "offer_accepted"
        property.buyer_id = self.partner_id
        property.selling_price = self.price

        for other in property.offer_ids: # only accept one offer
            other.status = "refused"
        self.status = "accepted"

    def action_refuse(self):
        for rec in self:
            rec.status = "refused"

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for rec in self:
            start_date = rec.create_date or fields.Date.today()
            rec.date_deadline = start_date + relativedelta(days = rec.validity)

    def _inverse_date_deadline(self):
        for rec in self:
            end, start = fields.Date.to_date(rec.date_deadline), fields.Date.to_date(rec.create_date)
            rec.validity = (end - start).days

    @api.model
    def create(self, vals):
        # NOTE: doesn't use `self.env[model_name].browse(value)` (?) as suggested in tuto but seems to work?
        new_offers = super().create(vals)
        for rec in new_offers:
            if rec.property_id.state == "new":
                rec.property_id.state = "offer_received"
        return new_offers


