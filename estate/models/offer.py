from odoo import api, fields, models
from odoo.tools import date_utils
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offer"
    _order = 'price desc'

    price = fields.Float('Price', copy=False)
    validity = fields.Integer('Validity Period of the Offer', default=7)
    date_deadline = fields.Date('Deadline for this offer', compute="_compute_deadline", inverse="_inverse_deadline", required=True)
    state = fields.Selection(
        string='Status',
        selection=[('draft', 'Draft'), ('accepted', 'Accepted'), ('refused', 'Refused')],
        default='draft',
        required=True
    )
    buyer_id = fields.Many2one('res.partner', string='Buyer', required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(related='property_id.type_id', store=True)

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The price for the offer must be strictly positive'
    )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            property = record.property_id
            if property.state == 'new':
                property.state = 'offer_received'
        return records

    @api.ondelete(at_uninstall=False)
    def _unlink_except_accepted_offer(self):
        if any(offer.state == 'accepted' for offer in self):
            raise UserError("Can't delete accepted offer")

    def _util_from_date(self):
        self.ensure_one()
        return self.create_date or fields.Datetime.today()

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = date_utils.add(record._util_from_date(), days=+record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record._util_from_date().date()).days

    def action_accept(self):
        for record in self:
            property = record.property_id
            if property.state not in ['sold', 'cancelled']:
                property.selling_price = record.price
                property.state = 'offer_accepted'
                property.offer_ids.state = 'refused'
                property.buyer_id = record.buyer_id
                record.state = 'accepted'
        return True

    def action_refuse(self):
        for record in self:
            record.state = 'refused'
        return True
