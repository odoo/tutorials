from odoo import api, fields, models


class PropertyType(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _check_positive_price = models.Constraint(
        "CHECK(price > 0)",
        "The offer price must be stricly positive",
    )

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer("Validity (Days)", default=7)
    date_deadline = fields.Date(
        compute="_compute_deadline",
        inverse="_inverse_deadline",
    )

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = fields.Date.add(create_date, days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.validity = (
                record.date_deadline - fields.Date.to_date(create_date)
            ).days

    # ------------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------------

    def action_accept_offer(self):
        for record in self:
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer = record.partner_id

            for offer in record.property_id.offer_ids:
                if offer != record:
                    offer.status = "refused"

        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = "refused"
        return True
