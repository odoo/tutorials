from odoo import fields, models, api
from odoo.tools.date_utils import add
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers for propreties"
    _order = "price desc"

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'Offer price must be strictly positive.',
    )
    price = fields.Float(required=True)
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    create_date = fields.Date(default=fields.Date.today(), readonly=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(related="property_id.type_id")

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = add(record.create_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days

    def action_accept_offer(self):
        self.ensure_one()
        self.status = 'accepted'
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        return 1

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
        return 1

    @api.model
    def create(self, vals):
        for val in vals:
            created_property = self.env['estate.property'].browse(val['property_id'])
            if any(float_compare(val['price'], offer.price, 0) < 0 for offer in created_property.offer_ids):
                raise ValidationError("A bigger offer already exists")
            if created_property.state == 'new':
                created_property.state = 'received'
        return super().create(vals)
