from odoo import models, fields, api
from datetime import timedelta, date

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = ''

    price = fields.Float()
    status = fields.Selection([
        ('accepted','Accepted'),
        ('refused','Refused'),
    ],
        copy=False,
    )
    validity = fields.Integer(string="Validity (Days)",default=7)

    # Relations
    partner_id = fields.Many2one(comodel_name='res.partner', required=True)
    property_id = fields.Many2one(comodel_name='estate.property', required=True)

    # computed 
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    #region Compute methodes
    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if not record.create_date:
                record.create_date = fields.Date.today()
            record.date_deadline = record.create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if not record.create_date:
                record.create_date = fields.Date.today()
            record.validity = (record.date_deadline - record.create_date.date()).days
    
    #endregion
