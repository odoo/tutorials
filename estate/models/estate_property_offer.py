from odoo import api, exceptions, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], readonly=True)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(
        string="Validity (days)",
        default=7,
    )
    date_deadline = fields.Date(
        compute="_compute_deadline",
        inverse="_compute_validity",
        string="Deadline",
    )

    _offer_price_positive_constraint = models.Constraint(
        "CHECK (price > 0)", "An offer price must be positive"
    )

    @api.depends("date_deadline", "create_date")
    def _compute_validity(self):
        for record in self:
            date_created = fields.Date.to_date(record.create_date) if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - date_created).days

    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for record in self:
            date_created = fields.Date.to_date(record.create_date) if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(date_created, days=record.validity)

    def action_confirm(self):
        if not any(offer.status == 'accepted' for offer in self.property_id.offer_ids):
            self.status = 'accepted'
            self.property_id.buyer_id = self.partner_id
            self.property_id.selling_price = self.price
        else:
            raise exceptions.UserError("Only one offer can be accepted at a time")
        return True

    def action_refuse(self):
        self.status = 'refused'
        if not any(offer.status == 'accepted' for offer in self.property_id.offer_ids):
            self.property_id.buyer_id = False
            self.property_id.selling_price = 0
        return True
