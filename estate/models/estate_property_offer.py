from datetime import timedelta
from odoo import _,fields,models,api
from odoo.exceptions import UserError, ValidationError


class EstatePropertytOffer(models.Model):
    _name = "estate.property.offer"
    _description ="It defines the estate property Offer"
    _order="price desc"

    price= fields.Float(copy=False, string='Price')
    status= fields.Selection(selection=[('accepted','Accepted'), ('refused','Refused')], string='Status', copy=False)
    partner_id= fields.Many2one('res.partner', string="Partner", required=True)
    property_id= fields.Many2one('estate.property', string='Property', required=True)
    validity= fields.Integer(default=7)
    property_status = fields.Selection(related='property_id.state', string='Property Status', store=True)
    date_deadline= fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one(string="Property Type",related='property_id.property_type_id',store=True)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            property_record = record.property_id
            if property_record.state == 'sold':
                raise UserError(_("Can't add a new offer to already sold property"))
            if record.price< property_record.best_price:
                raise UserError(_(f"Offer price must be greater than existing best price ({property_record.best_price})"))
            if property_record.state == 'new':
                property_record.write({'state': 'offer_received'})
        return records

    @api.depends('create_date','validity')
    def _compute_date_deadline(self):
        for record in self:
            create_date=record.create_date or fields.Datetime.today()
            record.date_deadline= create_date.date() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date= record.create_date or fields.Datetime.today()
            record.validity=(record.date_deadline-create_date.date()).days

    def action_accept(self):
        for record in self:
            if record.filtered(lambda self: self.status == 'accepted'):
                raise UserError(_("An offer has already been accepted for this property."))
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
        return True

    def action_reject(self):
        for record in self:
            record.status = 'refused'
        return True
