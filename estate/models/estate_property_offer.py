from odoo import models, fields

class EstatePropertyOffer(models.Model):
  _name = 'estate.property.offer'
  _description = 'this is estate property offer Database model created by meem (meet moradiya)...'

  price = fields.Float('Price')
  status = fields.Selection(
    string='Status',
    copy='False',
    selection=[
      ('accepted', 'Accepted'),
      ('refused', 'Refused')
    ]
  )
  partner_id = fields.Many2one('res.partner', 'Buyer ID', required=True)
  property_id = fields.Many2one('estate.property', 'Property ID', required=True)
