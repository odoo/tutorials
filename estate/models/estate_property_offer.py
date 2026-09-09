from odoo.exceptions import UserError
from odoo import api, fields, models
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [
            ('accepted', 'Acccepted'),
            ('refused', 'Refused'),
        ]
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    property_type_id = fields.Many2one(
        related="property_id.property_type_id",
        store=True,
    )

    _check_offer_price = models.Constraint(
        'CHECK(price > 0)',
        "Offer price must be strictly positive.",
    )

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for offer in self:
            create_date = offer.create_date or fields.Date.today()
            offer.date_deadline = create_date + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            create_date = offer.create_date.date() or fields.Date.today()
            if offer.date_deadline and create_date:
                offer.validity = (offer.date_deadline - create_date).days

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            current_price = vals.get('price')
            property_id = self.env['estate.property'].browse(
                vals['property_id'])
            for offer in property_id.offer_ids:
                if current_price < offer.price:
                    error_msg = f"The offer must be higher than the current highest offer {offer.price}."
                    raise UserError(error_msg)
            if property_id.state == 'new':
                property_id.state = 'offer_received'
        return super().create(vals_list)

    def action_accept(self):
        for record in self:
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"

            self.env['estate.property.booking'].create({
                'property_id': record.property_id.id,
                'buyer_id': record.partner_id.id,
            })
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True
