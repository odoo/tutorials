from odoo import api, models, fields
from datetime import date


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        string='Status',
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partener", required=True)
    property_id = fields.Many2one("estate.property", string="Property Id", required=True)
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(compute="_compute_total", inverse="_inverse_date_deadline", string="Deadline")
    property_type_id = fields.Many2one('estate.property.type', related="property_id.property_type_id", string="Property Type", store=True)

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'A Offer price must be strictly positive'),
    ]

    @api.depends("validity")
    def _compute_total(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date, days=record.validity)
            else:
                record.date_deadline = fields.Date.add(date.today(), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = fields.Date.subtract(record.date_deadline-fields.Date.to_date(record.create_date)).days

    def accept_icon(self):
        for record in self:
            record.status= 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.status = 'offer accepted'
            for offer in record.property_id.offer_ids:
                if offer.id != record.id:
                    offer.status= 'refused'
        return True

    def refuse_icon(self):
        for record in self:
            record.status = 'refused'
        return True