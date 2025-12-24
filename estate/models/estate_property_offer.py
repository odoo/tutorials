from odoo import api, fields, models
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float(name="Price")
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], string='Status', copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    # Functions
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date, days=record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept(self):
        for record in self:
            if record.property_id.state == 'offer accepted' or record.property_id.state == 'sold':
                msg = "An offer has already been accepted for this property!"
                raise UserError(msg)
            record.status = 'accepted'
            record.property_id.state = 'offer accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True

    @api.model_create_multi
    def create(self, vals):
        offer = super().create(vals)
        property_record = offer.property_id
        if property_record.state == 'new':
            property_record.state = 'received offer'
        else:
            if offer.price < property_record.best_price:
                msg = "Your offer is lower than an existing offer!"
                raise UserError(msg)
        return offer

    # Constraints
    _check_offer_price = models.Constraint('CHECK (price > 0)', "An offer price must be strictly positive")
