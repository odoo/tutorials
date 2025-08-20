from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offre d'achat"
    _order = "price desc"

    price = fields.Float("price")
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    date_deadline = fields.Date(default=lambda s:fields.Date.today() + relativedelta(days=7), compute="_compute_deadline", inverse="_update_validity")
    validity = fields.Integer(default=7)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    _sql_constraints = [
        ("positive_offer_price", "CHECK(price > 0)", "Offer should have a strictly positive price !")
    ]

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            now = record.create_date
            record.date_deadline = now + relativedelta(days=record.validity)

    def _update_validity(self):
        for offer in self:
            offer.validity = (offer.date_deadline - offer.create_date.date()).days

    def action_confirm(self):
        for offer in self:
            if offer.status == 'refused':
                raise UserError("You cannot accept an offer that is already refused.")
            other_offers = offer.property_id.offer_ids.filtered(lambda o: o.id != offer.id and o.status != 'refused')
            other_offers.write({'status': 'refused'})
            offer.write({'status': 'accepted'})
            offer.property_id.write({
                'buyer': offer.partner_id,
                'selling_price': offer.price,
            })
        return True

    def action_cancel(self):
        for offer in self:
            if offer.status == "accepted":
                raise UserError(self.env._("Offer already accepted"))
            offer.status = "refused"
        return True

    @api.model_create_multi
    def create(self, vals_list):
        properties = self.env['estate.property'].browse([vals['property_id'] for vals in vals_list])
        property_map = {prop.id: prop for prop in properties}
        for vals in vals_list:
            prop = property_map.get(vals['property_id'])
            if not prop:
                raise UserError("Invalid property_id in offer.")
            if prop.best_price and vals['price'] < prop.best_price:
                raise UserError("The price of a new offer can't be below the price of an already existing offer.")
        new_properties = properties.filtered(lambda p: p.state == 'new')
        new_properties.write({'state': 'offer_received'})
        return super().create(vals_list)
