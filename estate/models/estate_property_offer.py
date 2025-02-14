from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "Offer price must be strictly positive")
    ]

    price = fields.Float(string="Price")
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string="Status", copy=False)
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    partner_id = fields.Many2one(comodel_name="res.partner", required=True)
    property_id = fields.Many2one(comodel_name="estate.property")
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    # === COMPUTE METHODS === #
    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add((record.create_date or fields.date.today()), days=record.validity)
    
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days if record.date_deadline else 0

    # === Create Methods === #
    @api.model_create_multi
    def create(self,vals):
        for record in vals:
            property_id = self.env['estate.property'].browse(record['property_id'])
            if property_id:
                property_id.write({'state' : 'offerreceived'})

            if property_id.best_offer > record['price']:
                raise UserError("Offer Price entered is lower than the existing offer price.")

        return super().create(vals)

    # === Actions === #
    def action_accepted(self):
        # accepted_offer = self.search([('property_id', '=', self.property_id.id),('status', '=', 'accepted')], limit=1)
        #no need to find accepted offer just check the state to check if any offer is accepted
        if self.property_id.state == 'offeraccepted':
            raise ValidationError("An offer is already accepted, you cannot accept two offer for the same advertisement.")
        self.status = "accepted"
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        self.property_id.state = 'offeraccepted'

    def action_refused(self):
        self.status = "refused" 
