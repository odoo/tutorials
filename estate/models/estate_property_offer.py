from odoo import fields, models, api,exceptions
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for property"
    _order = "price desc"

    price = fields.Float()
    status= fields.Selection(
        selection=[("accepted","Accepted"), ("refused","Refused")],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property',required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline",inverse="_inverse_date_deadline", store=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                    delta = record.date_deadline - fields.Date.today()
                    record.validity = delta.days
            else:
                record.validity=7
    
    def action_confirm(self):
        for record in self:
            record.property_id.offer_ids.status = 'refused'
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            return True

    def action_cancel(self):
        for record in self:
            record.status = "refused"
        return True

    @api.model_create_multi
    def create(self, vals_list):
        offers = super().create(vals_list)
        for offer in offers:
            existing_offers = self.search([("property_id", "=", offer.property_id.id)])
            max_offer = max(existing_offers.mapped("price"),default=0)
            if existing_offers and offer.price < max_offer:
                raise ValidationError(f"Offer must be higher than {max_offer}")
            offer.property_id.state = "offer_received"
        return offers

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)',
         'Offer Price must be strictly positive.')
    ]
