from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError


class propertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers for the Real Estate Property"
    _order = "price desc"

    price = fields.Float("Price")
    status = fields.Selection(
        string="Status",
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True, string="Partner")
    property_id = fields.Many2one('estate.property', string="Property")
    validity = fields.Integer("Validity (Days)", default=7)
    date_deadline = fields.Date("Deadline", compute="_deadline_date_count", inverse="_inverse_deadline", store=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Offer Id", related="property_id.property_type_id", store=True)

    _sql_constraints = [('check_price', 'CHECK(price > 0)', 'Offer Price must be Positive')]

    @api.depends('validity')
    def _deadline_date_count(self):
        current_date = fields.Date.today()
        for record in self:
            record.date_deadline = current_date + relativedelta(days=record.validity)

    @api.model
    def create(self, vals):
        property_record = self.env['estate.property'].browse(vals['property_id'])
        if property_record.offer_ids:
            max_price = max(property_record.offer_ids.mapped('price'))
            if vals['price'] < max_price:
                raise UserError(f"offer price should be more than {max_price}")
        return super().create(vals)

    def _inverse_deadline(self):
        current_date = fields.Date.today()
        for record in self:
            record.validity = relativedelta(record.date_deadline, current_date).days

    def action_accepted(self):
        if not self.property_id.buyer_id:
            if self.price < self.property_id.expected_price * 0.9:
                raise ValidationError("Selling Price is too Low")
            self.status = 'accepted'
            self.property_id.selling_price = self.price
            self.property_id.buyer_id = self.partner_id
            self.property_id.state = 'offer_accepted'
        else:
            raise UserError("Offer has been already Accepted")

    def action_refused(self):
        if self.property_id.buyer_id == self.partner_id:
            self.property_id.buyer_id = ''
            self.property_id.selling_price = 0
        self.status = 'refused'

    def unlink(self):
        for record in self:
            if record.status == 'accepted':
                record.property_id.buyer_id = ''
                record.property_id.selling_price = 0
        return super().unlink()
