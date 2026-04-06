from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "estate property offers"
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(
        [('accepted', "Accepted"), ('refused', "Refused")], copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    property_type_id = fields.Many2one(
        'estate.property.type', related='property_id.property_type', store=True
    )
    date_deadline = fields.Date(
        compute='_compute_date_deadline', inverse='_inverse_date_deadline'
    )
    _chek_offer_price = models.Constraint(
        'CHECK(price > 0)', 'offer price of property should be positive'
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(
                record.create_date or fields.Date.today(), days=record.validity
            )

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept(self):
        if any(record.property_id.state == "offer_accepted" for record in self):
            raise UserError("One offer is already accepted for this property.")

        for record in self:
            property_obj = record.property_id

            property_obj.write(
                {
                    "buyer_id": record.partner_id.id,
                    "selling_price": record.price,
                    "state": "offer_accepted",
                }
            )
            record.status = "accepted"

            other_offers = property_obj.offer_ids - record
            other_offers.write({"status": "refused"})
        return True

    def action_refuse(self):
        self.status = 'refused'
        return True

    @api.model
    def create(self, vals):
        for val in vals:
            if (
                self.env["estate.property"]
                .browse(val["property_id"])
                .offer_ids.filtered(lambda x: x.price > val["price"])
            ):
                raise UserError(
                    "offer amount should be grater than current offer amount."
                )
            self.env['estate.property'].browse(
                val['property_id']
            ).state = 'offer_received'
        offers = super().create(vals)

        # Inside your offer creation or confirmation method
        for offer in self:
            if self.env['ir.module.module'].sudo().search([('name', '=', 'crm'), ('state', '=', 'installed')]):
                self.env['crm.lead'].sudo().create({
                    'name': offer.property_id.name,
                    'partner_id': offer.partner_id.id,
                    'expected_revenue': offer.price,
                    'type': 'lead', # Offers created as 'leads'
        })
        return offers
