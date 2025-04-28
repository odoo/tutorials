from odoo import models, fields, api, _
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate_property_offer"
    _description = "property offers"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate_property", string="Property", required=True)
    validity = fields.Integer(compute="_compute_validity", inverse="_inverse_validty")
    date_deadline = fields.Date(string="Deadline", required=True)
    property_type_id = fields.Many2one(related="property_id.estate_property_type", string="Property Type", store=True)

    _sql_constraints = [
        ('check_price_positive', 'CHECK(price > 0)', 'The price should be higher than 0'),
    ]

    @api.depends("date_deadline")
    def _compute_validity(self):
        today = fields.Datetime.today().date()
        for record in self:
            deadline = record.date_deadline
            if deadline:
                start_date = record.create_date.date() if record.create_date else today
                delta = deadline - start_date
                record.validity = delta.days
            else:
                record.validity = 0

    def _inverse_validty(self):
        for record in self:
            if record.create_date and record.validity:
                record.date_deadline = fields.Datetime.add(record.create_date, days=record.validity)

    def action_confirm(self):
        for offer in self:
            if offer.property_id.state in ['sold', 'canceled']:
                raise UserError("You can't validate an offer for a sold property")
            else:
                offer.property_id.write({
                    'buyer_id' : offer.partner_id,
                    'selling_price' : offer.price,
                    })
                offer.status = 'accepted'
                offer.property_id.mark_as_sold()
            related_offers = offer.property_id.offer_ids.filtered(lambda o: o.id != offer.id and o.status != 'refused')
            related_offers.action_close()

    def action_close(self):
        self.write({'status': 'refused'})

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get('property_id')
            price = vals.get('price')

            property = self.env['estate_property'].browse(property_id)

            if any(price < best_price for best_price in property.best_price):
                raise UserError(_("You can't create an offer with a lower price than an existing offer"))
            
        return super().create(vals_list)
