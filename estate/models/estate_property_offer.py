from odoo import api, models, fields
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class estate_offer(models.Model):
    _name = "estate.property.offer"
    _description = "This is Real Estate property offer"
    _order = "price desc"

    price = fields.Float("Price")
    status = fields.Selection(
        string="status",
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)

    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date("Date Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            current_date = fields.Date.today()
            record.date_deadline = current_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            current_date = fields.Date.today()
            if record.date_deadline:
                record.validity = relativedelta(record.date_deadline, current_date).days
            else:
                record.validity = 0

    def action_accept(self):
        if self.property_id.buyer_id:
            raise UserError("only one offer accepted")
        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id

    def action_refuse(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.buyer_id = ""
                record.property_id.selling_price = 0.0
            record.status = "refused"

    _sql_constraints = [
        ('offer_price', 'CHECK(price > 0)',
         'offer price must be strictly positive')
    ]

    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", string="Offers", stored=True)

    @api.model
    def create(self, vals):
        property_id = vals.get('property_id')
        offer_price = vals.get('price')

        property_record = self.env['estate.property'].browse(property_id)

        existing_offers = self.search([
            ('property_id', '=', property_id),
            ('price', '>=', offer_price)
        ])
        if existing_offers:
            raise UserError('You cannot create an offer with a lower or equal amount than an existing offer.')

        property_record.state = 'offer_received'

        return super().create(vals)
