from odoo import models , fields 

class PromiseDateRecord(models.Model):
    _name='promise.date.record'
    _description="Store records of the promise date"

    sale_order_id = fields.Many2one('sale.order', string="Sale Order", ondelete='cascade')
    changed_by = fields.Many2one('res.users', string="Changed By", default=lambda self: self.env.user)
    changed_on = fields.Date(string="Changed On", default=fields.Datetime.now)
    from_date = fields.Date(string="Previous Revised Promise Date")
    to_date = fields.Date(string="New Revised Promise Date")
    