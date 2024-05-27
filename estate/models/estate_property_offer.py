from odoo import fields, models, api

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "estate property offers"

    # simple fields
    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', "Accepted"),
                   ('refused', "Refused"),
                   ],
        copy=False,
        )
    validity = fields.Integer("Validity (Days)", default=7)

    # relational fields
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    
    #computed fields
    date_deadline = fields.Date("Deadline Date", compute= '_compute_deadline', inverse='_inverse_deadline')

    #compute methods
    @api.depends('validity', 'create_date')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.create_date, days=record.validity) if record.create_date \
            else fields.Date.add(fields.Datetime.today(), days = record.validity)
            
    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days