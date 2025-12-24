import datetime

from odoo import api, exceptions, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real estate property offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True, string="Sales")
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )
    property_type_id = fields.Integer(
        related="property_id.property_type_id.id", store=True
    )

    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "The offer price for a property has to be positive",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (
                record.create_date.date()
                if record.create_date
                else datetime.date.today()
            ) + datetime.timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_confirm(self):
        for record in self:
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "offer_accepted"
            record.property_id.reject_other_offers(record)

    def action_cancel(self):
        for record in self:
            record.status = "refused"

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            prop = self.env['estate.property'].browse(vals['property_id'])
            if prop.lowball_offer(vals['price']):
                raise exceptions.UserError("Offer price can't be lower than lowest offer")
            prop.state = "offer_received"
        return super().create(vals_list)
