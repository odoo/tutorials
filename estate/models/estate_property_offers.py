from odoo import fields, models, api, exceptions


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offers"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        [("Accepted", "accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_deadline", inverse="_inverse_deadline", store=True
    )

    # date_deadline
    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(
                    record.create_date, days=record.validity
                )
            # if user adding new data then their is no available of create_date then use today
            else:
                record.date_deadline = fields.Date.add(
                    fields.Date.today(), days=record.validity
                )

    def _inverse_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (
                    record.date_deadline - record.create_date.date()
                ).days
            else:
                record.validity = (
                    record.date_deadline - record.fields.Date.today()
                ).days

    def action_accepted(self):
        for record in self:
            # selling price is default 0 and field is readonly then when the selling_price 0 so their is no offer is accepted yet
            if record.property_id.selling_price == 0:
                record.status = "Accepted"
                record.property_id.selling_price = record.price
                record.property_id.buyer = record.partner_id
                record.property_id.state = "offer_accepted"
            else:
                raise exceptions.UserError("Already One Offer is Accepted")

    def action_refused(self):
        for record in self:
            record.status = "refused"
