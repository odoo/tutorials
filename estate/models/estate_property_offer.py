from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date("Deadline", compute="_calculate_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id", stored=True)

    _check_price = models.Constraint("CHECK(price>0)", "The selling price needs to be bigger then 0")

    @api.depends("validity", "create_date")
    def _calculate_date_deadline(self):
        for offer in self:
            offer.date_deadline = (offer.create_date or fields.Date.today()) + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - fields.Date.today()).days

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            self.env["estate.property"].browse(vals["property_id"]).offer_made(vals["price"])
        return super().create(vals_list)

    def action_accept_offer(self):
        self.ensure_one()
        if self.status:
            raise UserError("The offer was already revised")
        self.property_id.accept_offer(self.price, self.partner_id)
        self.status = "accepted"

    def action_refuse_offer(self):
        self.ensure_one()
        if self.status:
            raise UserError("The offer was already revised")
        self.status = "refused"
