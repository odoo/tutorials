# type: ignore
from datetime import timedelta
from odoo import api,fields,models 
from odoo.exceptions import UserError 


class estatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

    price=fields.Float(string="Price")
    status=fields.Selection(
        selection=[
            ('accepted','Accepted'),
            ('refused','Refused')
        ])
    partner_id=fields.Many2one('res.partner',string="Partner",required=True, ondelete="cascade")
    property_id = fields.Many2one("estate.property", required=True, string="Property" )
    validity = fields.Integer(string="Validity(Days)",default="7")
    date_deadline = fields.Date(string="Deadline",compute="_compute_date_deadline",inverse="_inverse_date_deadline",store=True)

    #sql constraints
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'The offer price must be strictly positive.'),
    ]

    #compute dealine
    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            for record in self:
              record.date_deadline = (record.create_date or fields.Date.today()) + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = 7

    #logic for offer accepted or refused
    def action_accept_offer(self):
        """Accept an offer and update the property."""
        for record in self:
            if record.property_id.selling_price:
                raise UserError("This property already has an accepted offer!")

            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.status = "sold"
        return True

    def action_refuse_offer(self):
        """Refuse an offer."""
        for record in self:
            record.status = "refused"
        return True
