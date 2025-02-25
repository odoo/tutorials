from dateutil.relativedelta import relativedelta
from odoo import api, models, fields
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(string="Status", copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline")
    property_type_id = fields.Many2one('estate.property.type', related="property_id.property_type_id", store=True)

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'The offer price must be stricty positive.')
    ]

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if record.date_deadline:
                record.validity = (record.date_deadline - fields.Date.today()).days
            else:
                record.validity = 7

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            best_offer_price = self.env['estate.property'].browse(vals['property_id']).best_offer
            property_state = self.env['estate.property'].browse(vals['property_id']).state

            if property_state == 'sold' or property_state == 'invoiced':
                raise UserError("You cannot create offer for sold or invoiced property")

            if best_offer_price:
                if vals.get('price') < best_offer_price:
                    raise UserError(f"The offer must be higher than best offer {best_offer_price}")

            self.env['estate.property'].browse(vals['property_id']).state = 'offer_received'
        return super(EstatePropertyOffer, self).create(vals_list)

    # Action Button Methods
    def action_set_offer_status_accepted(self):
        if self.status == 'accepted' or self.status == 'refused':
            raise UserError("Property is already accepted or refused.")
        else:
            self.property_id.property_offer_ids.status = 'refused'

            self.property_id.selling_price = self.price
            self.property_id.buyer = self.partner_id
            self.property_id.state = 'offer_accepted'
            self.status = 'accepted'

    def action_set_offer_status_refused(self):
        if self.status == 'accepted' or self.status == 'refused':
            raise UserError("Property is already accepted or refused.")
        else:
            self.status = 'refused'
                