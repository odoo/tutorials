from odoo.exceptions import UserError
from odoo.tools.date_utils import add
from odoo import _, api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer model"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    partner_id = fields.Many2one("res.partner", required=True, string="Partner")
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        string="Deadline",
    )
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", string="Property Type", store=True)

    _offer_price_strictly_positive_constraint = models.Constraint("CHECK(price > 0)", "The price of an offer should be strictly greater than 0!")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = add(base_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else fields.Date.today()
            if record.date_deadline and base_date:
                record.validity = (record.date_deadline - base_date).days

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get("property_id")
            price = vals.get("price")

            if property_id and price:
                property_obj = self.env["estate.property"].browse(property_id)
                if property_obj.offer_ids:
                    max_offer = max(property_obj.offer_ids.mapped("price"))
                    if price <= max_offer:
                        raise UserError(_("The offer amount must be strictly higher than the maximum existing offer."))

        records = super().create(vals_list)

        for record in records:
            if record.property_id:
                record.property_id.state = "offer_received"

        return records

    def accept_offer(self):
        for record in self:
            accepted_offer = record.property_id.offer_ids.filtered(lambda offer: offer.status == "accepted")
            if accepted_offer:
                raise UserError(_("Only one offer can be accepted for a giver property !"))
            record.status = "accepted"
            record.property_id.buyer = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"
        return True

    def refuse_offer(self):
        self.status = "refused"
        return True
