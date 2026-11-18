from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Offer"
    _order = "price desc"
    _check_price = models.Constraint("CHECK (price > 0)",
                                    "The price of an offer needs to be strictly positive")

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )

    create_date = fields.Date(default=fields.Date.today())
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    
    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.create_date, days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date).days
            else:
                record.validity = 0

    def action_accept_offer(self):
        for record in self:
            # All of the offers we accepted previously are reverted to refused
            record.property_id.offer_ids.filtered(lambda o: o.status == "accepted").status = "refused"

            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
        return True
