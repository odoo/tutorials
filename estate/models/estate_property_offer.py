from odoo import fields, models, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer to buy a real estate property"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id")

    _sql_constraints = [
        ('positive_offer_price', 'CHECK(price >= 0)', 'The offer price price must be positive')
    ]

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for offer in self:
            try:
                offer.date_deadline = fields.Date.add(offer.create_date, days=offer.validity)
            except:
                offer.date_deadline = fields.Date.add(fields.Date.today(), days=offer.validity)

    @api.depends('create_date', 'date_deadline')
    def _compute_validity(self):
        for offer in self:
            try:
                offer.validity = (offer.date_deadline - fields.Date().to_date(offer.create_date)).days
            except:
                offer.validity = (offer.date_deadline - fields.Date().today()).days

    def _inverse_deadline(self):
        for offer in self:
            offer.date_deadline = offer.date_deadline

    def _inverse_validity(self):
        for offer in self:
            offer.validity = offer.validity

    validity = fields.Integer(default=7, compute=_compute_validity, inverse=_inverse_validity)
    date_deadline = fields.Date(compute=_compute_deadline, inverse=_inverse_deadline)

    def action_accept_offer(self):
        if 'accepted' in self.property_id.offer_ids.mapped('status'):
            raise UserError('This property already has an accepted offer')

        self.status = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id.user_id
        return True

    def action_refuse_offer(self):
        self.status = 'refused'
        return True

    @api.model_create_multi
    def create(self, valses):
        for vals in valses:
            estate_property = self.env["estate.property"].browse(vals["property_id"])
            print(vals["price"], max(estate_property.offer_ids.mapped("price")))
            if max(estate_property.offer_ids.mapped("price")) > vals["price"]:
                raise UserError("Cannot offer less than the best offer.")
            else:
                estate_property.state = "offer_received"
                
        return super(EstatePropertyOffer, self).create(valses)
