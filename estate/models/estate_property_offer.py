from odoo import api, models, fields
from datetime import timedelta 
from odoo.exceptions import UserError
class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "Offer price must be strictly positive."),
    ] 

    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Status",
        copy=False
    )

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
               start_date = fields.Date.to_date(offer.create_date)
               offer.date_deadline = start_date + timedelta(days=offer.validity)
            else:
               offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline and offer.create_date:
              start_date = fields.Date.to_date(offer.create_date)
            offer.validity = (offer.date_deadline - start_date).days

    def action_accept(self):
        for offer in self:
            if offer.property_id.state in ('canceled', 'sold'):
                raise UserError("Cannot accept offers for canceled or sold properties.")
            accepted_offers = self.env['estate.property.offer'].search([
                ('property_id', '=', offer.property_id.id),
                ('status', '=', 'accepted')
            ])
            if accepted_offers:
                raise UserError("Another offer is already accepted for this property.")
            offer.status = 'accepted'
            # Update property's selling price and buyer
            offer.property_id.write({
                'selling_price': offer.price,
                'buyer_id': offer.partner_id.id
            })
            # Refuse other offers
            other_offers = self.env['estate.property.offer'].search([
                ('property_id', '=', offer.property_id.id),
                ('id', '!=', offer.id)
            ])
            other_offers.write({'status': 'refused'})
        return True

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
        return True