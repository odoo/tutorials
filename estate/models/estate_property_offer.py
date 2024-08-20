from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "This model stores estate property offers information (buyer, price, date, status)"
    _order = "price desc"
    _sql_constraints = [
        ('price_check', 'CHECK (price > 0)', 'the price must be strictly positive')
    ]

    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Title", required=True)
    property_type_id = fields.Many2one("estate.property.type", string="Type", related="property_id.property_type_id", store=True)

    price = fields.Float(string="Offer Price")
    status = fields.Selection(string="Status", copy=False, selection=[
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ])
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = fields.Datetime.add(offer.create_date, days=offer.validity)
            else:
                offer.date_deadline = fields.Datetime.add(fields.Datetime.today(), days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (fields.Date.to_date(offer.date_deadline) - fields.Date.to_date(offer.create_date)).days

    @api.model
    def create(self, vals):
        estate_property = self.env['estate.property'].browse(vals['property_id'])
        if estate_property.state in ('new', 'offer_received'):
            estate_property.state = 'offer_received'
            if estate_property.best_price > vals['price']:
                raise UserError(_("A better offer already exists"))
            else:
                return super().create(vals)
        else:
            raise UserError(_("A property can't receive another offer after accepting one"))

    def estate_property_offer_button_accept(self):
        for offer in self:
            offer.status = "accepted"
            other_offers = self.search([
                ('property_id', '=', offer.property_id.id),
                ('id', '!=', offer.id)
            ])
            other_offers.write({'status': 'refused'})
            offer.property_id.state = 'offer_accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id

    def estate_property_offer_button_refuse(self):
        for offer in self:
            offer.status = "refused"
