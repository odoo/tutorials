from odoo import api, fields, models
from odoo.tools import date_utils
from odoo.exceptions import UserError, ValidationError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'The offer price should be positive.')
    ]
    _order = "price desc"


    price = fields.Float(string="Price")
    status = fields.Selection(string="Status", copy=False, selection=[
        ('accepted', "Accepted"),
        ('refused', "Refused"),
    ])
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(compute="_compute_deadline_date", inverse="_inverse_deadline_date", string="Deadline")

    property_type_id = fields.Many2one(related="property_id.type_id", string="Property Type")

    @api.depends("validity", "property_id.create_date")
    def _compute_deadline_date(self):
        for record in self:
            if record.property_id.create_date:
                record.date_deadline = date_utils.add(record.property_id.create_date, days=record.validity)
            else:
                record.date_deadline = fields.Date.today()


    @api.depends("date_deadline", "property_id.create_date")
    def _inverse_deadline_date(self):
        for record in self:
            record.validity = (record.date_deadline - record.property_id.create_date.date()).days

    @api.model
    def create(self, vals):
        new_offer_price = vals.get('price')
        property_id = vals.get('property_id')
        if property_id:
            existing_offers = self.env['estate.property'].browse(property_id).offer_ids
            max_price = max(existing_offers.mapped('price'), default=0)

        if new_offer_price <= max_price:
            raise ValidationError("New offer price must be higher than existing offers.")

        return super().create(vals)

    def action_accept_offer(self):
        for record in self:
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"

        (self.property_id.offer_ids - self).write({'status': 'refused'}) # refusing all other offers

        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = "refused"

        return True
