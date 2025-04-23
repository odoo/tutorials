from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float("Price")
    state = fields.Selection(
        "State",
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused")
        ], copy=False
    )
    partner_id = fields.Many2one('res.partner',
                                 "Partner",
                                 required=True)
    property_id = fields.Many2one("estate.property",
                                  "Property",
                                  required=True)
    date_deadline = fields.Date("Deadline Date",
                                compute='_compute_date_deadline',
                                inverse='_inverse_date_deadline')
    validity = fields.Integer("Validity Days", default=7)

    property_type_id = fields.Many2one('estate.property.type',
                                       related='property_id.type_id', store=True)
    _sql_constraints = [
        (
            "check_price_positive",
            "CHECK(price >= 0)",
            "Offer price must be strictly positive.",
        ),
    ]

    @api.depends("validity")
    def _compute_date_deadline(self):
        for val in self:
            val.date_deadline = datetime.now() + relativedelta(days=val.validity)

    def _inverse_date_deadline(self):
        for val in self:
            if val.create_date and val.date_deadline:
                val.validity = (
                        val.date_deadline - val.create_date.date()
                ).days
            else:
                val.validity = 7

    def action_accept(self):
        for val in self:
            self.property_id.offer_ids.filtered(
                lambda x: x.state == 'accepted').write({
                'state': 'refused',
            })

            val.state = 'accepted'
            val.property_id.write({
                'buyer_id': val.partner_id.id,
                'selling_price': val.price,
            })

    def action_refuse(self):
        for val in self:
            val.state = 'refused'
            val.property_id.write({
                'buyer_id': False,
                'selling_price': False,
            })
