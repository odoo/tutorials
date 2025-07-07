from odoo import api, fields, models
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers for estate property"
    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline", 
        compute="_compute_date_deadline", 
        inverse="_inverse_date_deadline"
    )
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Status",
        copy=False
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            start_date = record.create_date or fields.Date.context_today(record)
            record.date_deadline = fields.Date.add(start_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            start_date = record.create_date or fields.Date.context_today(record)
            if record.date_deadline:
                delta = record.date_deadline - start_date.date()
                record.validity = delta.days
            else:
                record.validity = 0
    
    def action_on_accepted(self):
        for offer in self:
            accepted_offers = offer.property_id.offer_ids.filtered(lambda o: o.status == 'accepted')
            if accepted_offers:
                raise UserError("An offer has already been accepted for this property.")
            
            offer.status = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.state = 'offer_accepted'
        return True

    def action_on_refused(self):
        for offer in self: 
            offer.status = "refused"
        return True