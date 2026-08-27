from odoo import _, api, fields, models
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"
    _order = "price desc"

    price = fields.Float()
    _check_price = models.Constraint(
            'check (price > 0)',
            'The offer price can not be negative or zero')
    status = fields.Selection(
            selection=[
                ('accepted', 'Accepted'),
                ('refused', 'Refused')],
            copy=False,
            help="State of the estate property offer")
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    property_type_id = fields.Many2one(
            'estate.property.type',
            related='property_id.property_type_id',
            store=True)

    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date(
            'Deadline',
            compute='_compute_date_deadline',
            inverse='_onchange_date_deadline',
            help='Deadline defined as date from creation separated by validy dates')

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date, days=record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Datetime.now(), days=record.validity)

    @api.onchange('date_deadline')
    def _onchange_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept_offer(self):
        for record in self:
            if any(o.status == 'accepted' for o in record.property_id.offer_ids):
                raise UserError(_("One does not simply accept multiple offers on the property"))

            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'

    def action_reset_status(self):
            for record in self:
                record.status = None

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            estate_property = self.env['estate.property'].browse(vals['property_id'])

            if vals['price'] < estate_property.best_price:
                raise UserError(f"You can not create an offer with lower price than est offer: {estate_property.best_price}")

            estate_property.state = 'offer_received';

        super().create(vals_list)
