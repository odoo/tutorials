from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(string="Price")
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string="Status", copy=False)
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    partner_id = fields.Many2one(comodel_name="res.partner", required=True)
    property_id = fields.Many2one(comodel_name="estate.property")

    # === COMPUTE METHODS === #
    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            # create_date = record.create_date if record.create_date else fields.Date.today()
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date, days=record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)
    
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days if record.date_deadline else 0

    # === Actions === #
    def action_accepted(self):
        accepted_offer = self.search([('property_id', '=', self.property_id.id),('status', '=', 'accepted')])
        if accepted_offer:
            raise UserError("An offer is already accepted, you cannot accept two offer for the same advertisement.")
        self.status = "accepted"
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price

    def action_refused(self):
        self.status = "refused"
        self.property_id.buyer_id = False
        self.property_id.selling_price = False      
