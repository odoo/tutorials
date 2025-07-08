from odoo import api, fields, models
from datetime import timedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        string="Type",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string='salesperson', required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", store=True)

    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "The price must be strictly positive.")
    ]
    
    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if not record.create_date:
                today = fields.Datetime.today()
                record.date_deadline = base_date + timedelta(days=record.validity)
            else:
                record.date_deadline = record.create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept_offer(self):
        for record in self:
            record.status = "accepted"
            if record.property_id:
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id
                record.property_id.state = "offer_accepted"
        return True

    def action_accept_offer(self):
        for offer in self:
            if offer.property_id.state in {'accepted', 'sold'}:
                raise UserError(_('An offer has already been accepted for this property.'))

            offer.write({'status': 'accepted'})

            offer.property_id.write({
                'selling_price': offer.price,
                'buyer_id': offer.partner_id.id,
                'state': 'offer_accepted',
            })

        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = "refused"
        return True
