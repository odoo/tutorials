from odoo import api, fields, models


class EstatePorpertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float()
    status = fields.Selection([
        ('accepted', 'Accepted'), ('refused', 'Refused')
    ])
    validity = fields.Integer(default=7)

    # Compute Fields
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    # Relational Fields
    partner_id = fields.Many2one("res.partner", "Partner", required=True)
    property_id = fields.Many2one("estate.property", "Property", required=True)

    # Compute Methods
    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(
                create_date, days=record.validity)

    # Inverse Methods
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline -
                               record.create_date.date()).days

    # Action Methods
    def action_set_offer_status_accept(self):
        self.ensure_one()
        self.status = 'accepted'
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        self._make_excluded_offers_refused()
        return True

    def action_set_offer_status_refuse(self):
        self.ensure_one()
        self.status = 'refused'
        return True

    # Helper Method : Refuse all offers except the current one
    def _make_excluded_offers_refused(self):
        for offer in self.property_id.offer_ids.filtered(lambda o: o.id != self.id):
            offer.status = 'refused'
