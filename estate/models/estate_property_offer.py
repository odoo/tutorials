from odoo import api, fields, models
from odoo.exceptions import UserError

class PropertyOffer(models.Model):

    _name = "estate_property_offer"
    _description = "An offer to buy a real estate property"
    _sql_constraints = [
        ('check_positive_price', 'CHECK (price > 0)', 'The Price must be strictly positive'),
    ]
    _order = 'price desc'
    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('Accepted', 'Accepted'),
            ('Refused', 'Refused'),
        ],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate_property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline_date", inverse="_inverse_deadline_date")

    # No need to add creation_date to @api.depends, because the create date will never change.
    @api.depends("validity")
    def _compute_deadline_date(self):
        for record in self:
            record.date_deadline = fields.Date.add(
                record.create_date if record.create_date else fields.Date.today(),
                days=record.validity
            )

    def _inverse_deadline_date(self):
        for record in self:
            # No need to check whether record.create_date is present because the inverse function is called
            # when the record is saved, so the create date will be present.
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept(self):

        if "Accepted" in self.mapped('property_id.property_offer_ids.status'):
            raise UserError("There can only be one accepted offer")

        self.status = "Accepted"
        self.property_id.selling_price = self.price
        self.property_id.partner_id = self.partner_id
        self.property_id.state = "Offer Accepted"
        return True

    def action_refuse(self):

        self.status = "Refused"
        return True
