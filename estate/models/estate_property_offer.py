from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer module for Odoo 19 tutorials"

    price = fields.Float(required=True, string="Offer Price")
    status = fields.Selection([
        ("accepted", "Accepted"),
        ("refused", "Refused"),
    ], copy=False, string="Offer Status")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity (in days)", default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline")

    _check_offer_price_positive = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be strictly positive.',
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date.date(), days=record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept(self):
        self.ensure_one()
        self.status = "accepted"
        self.property_id.state = "offer_accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id

    def action_refuse(self):
        self.status = "refused"
