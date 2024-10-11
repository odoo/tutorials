from odoo import api, fields, models  # type: ignore
from datetime import timedelta, date

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer Ayve"

    price = fields.Float()
    status = fields.Selection(
    [
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ],
    string='Status',
    copy=False
    )

    partner_id = fields.Many2one(
        'res.partner',
        required=True,
        string="Partner"
    )

    property_id = fields.Many2one(
        'estate.property',
        required=True,
        string="Property ID"
    )

    validity =  fields.Integer(
        string="Validity(Days)",
        default=7
    )
    
    date_deadline=fields.Date(
        string="Dateline",
        compute="_compute_deadline",
        inverse="_inverse_deadline",
        store=True
    )

    # Compute Methods
    # when inverse is used the field becomes editable (not read only)
    # compute makes it read only
    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if not record.create_date:
                record.create_date = date.today()
            record.date_deadline = record.create_date.date() + timedelta(days=record.validity)

    # used the abs so the app wont crash when getting -ve number
    def _inverse_deadline(self):
        for record in self:
            record.validity=  abs((record.date_deadline - record.create_date.date()).days)
    
    #Action Button
    def action_accept_offer(self):
        for record in self:
            record.status = "accepted"
        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = "refused"
        return True


    