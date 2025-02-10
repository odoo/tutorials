from odoo import api, fields, models
from datetime import datetime, timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(string="Offer Price")
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], string="Offer Status", copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer(string="Validity (in days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_validity", store=True)
    create_date = fields.Date(readonly=True, default=fields.Date.today)



    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.validity is not None:
                record.date_deadline = datetime.now().date() + timedelta(days=record.validity)
            else:
                # If validity is not set, set the deadline to 7 days
                record.date_deadline = datetime.now().date() + timedelta(days=7)

    def _inverse_validity(self):
            for record in self:
                if record.create_date and record.date_deadline:
                    record.validity = (record.date_deadline - record.create_date).days



    # ------------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------------

    def action_offer_accept(self):
        for record in self:
            record.status = "accepted"
            record.property_id.state = "offer_accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer = record.partner_id

            other_offers = self.env['estate.property.offer'].search([
                ('property_id', '=', record.property_id.id),
                ('id', '!=', record.id),
                ('status', '!=', 'refused')
            ])
            other_offers.write({'status': 'refused'})
        return True

    def action_offer_refuse(self):
        self.status = "refused"
        return True
