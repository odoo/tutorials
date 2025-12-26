from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline')

    _price_pos = models.Constraint(
        "CHECK(price > 0)", "The offer price must be strictly positive."
    )

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.deadline = create_date + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.deadline - fields.Date.to_date(record.create_date)).days

    def action_confirm(self):
        self.status = 'accepted'
        for offer in self.property_id.offer_ids:
            if offer.id == self.id:
                continue

            offer.status = 'refused'

        self.property_id.state = 'offer_accepted'
        self.property_id.partner_id = self.partner_id
        self.property_id.selling_price = self.price
        return True

    def action_refuse(self):
        self.status = 'refused'
        return True

    @api.model_create_multi
    def create(self, vals):
        for record in vals:
            property = self.env['estate.property'].browse(record['property_id'])
            if property.state == 'sold':
                raise UserError(self.env._("You cannot create an offer for property that is already sold."))

            min_price = min(property.offer_ids.mapped('price')) if property.offer_ids else 0.0
            if record['price'] < min_price:
                raise UserError(self.env._("The offer must be higher than %d.", min_price))

            property.state = 'offer_received'

        return super().create(vals)
