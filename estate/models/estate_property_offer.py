from odoo import api, fields, models

class EstatePorpertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offer for Estate Poperty'

    price = fields.Float()
    status = fields.Selection(selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Estate Property", required=True)
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline',inverse='_inverse_date_deadline', string='Date Deadline')
    create_date = fields.Date(default=fields.Date.today())
    
    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date, days=record.validity)
            else:
                record.date_deadline = fields.Date.add(record.create_date, fields.Date.today())

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days
