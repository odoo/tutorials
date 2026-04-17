from datetime import timedelta

from odoo import api, fields, models

from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
        string="Current Status", copy=False)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True,)
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", store=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'Offer price must be strictly positive.'
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        today = fields.Date.today()
        for record in self:
            base_date = record.create_date.date() if record.create_date else today
            record.date_deadline = base_date + timedelta(days=record.validity or 0)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date.date()).days

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            property_rec = record.property_id
            existing_offers = property_rec.offer_ids - record
            if existing_offers:
                max_price = 0
                for offer in existing_offers:
                    if offer.price > max_price:
                        max_price = offer.price
                if record.price <= max_price:
                    raise UserError("Offer must be higher than existing offers.")
            property_rec.state = 'offer_received'
        return records

    def action_accept(self):
        for record in self:
            for offer in record.property_id.offer_ids:
                if offer.status == 'accepted':
                    raise UserError("Only one offer can be accepted for a property.")
            record.status = 'accepted'
            # record.property_id.selling_price = record.price
            # record.property_id.buyer_id = record.partner_id
            # record.property_id.state = 'offer_accepted'
            record.property_id.write({
            'selling_price': record.price,
            'buyer_id': record.partner_id.id,
            'state': 'offer_accepted'})
            (record.property_id.offer_ids - record).filtered(lambda offer: offer.status != 'refused').write({'status': 'refused'})
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
            # if record.property_id.buyer_id == record.partner_id:
            # record.property_id.write({
            #     'selling_price': 0,
            #     'buyer_id': False,
            #     'state': 'offer_received'
            # })
            record.property_id.selling_price = False
        return True
