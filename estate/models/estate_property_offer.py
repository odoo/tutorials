from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate property offer'

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Offer", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline", default=fields.Date.add(fields.Date.today(), days=7))

    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self.filtered("create_date"):
            record.date_deadline = fields.Date.add(record.create_date, days=record.validity)

    def _inverse_deadline(self):
        for record in self.filtered("create_date"):
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_btn_accept(self):
        self.ensure_one()
        self.status = "accepted"
        self.property_id.buyer_id = self.partner_id.id
        self.property_id.selling_price = self.price
        self.property_id.state = 'offer_accepted'

    def action_btn_refuse(self):
        for record in self:
            record.status = "refused"
        return True

    _check_positive_offer_price = (models.Constraint("""CHECK (price >= 0)""",
             "The property offer price must be positive."))
