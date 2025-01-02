from odoo import models, fields
from datetime import datetime
from dateutil.relativedelta import relativedelta
class test_model(models.Model):
    _name="estate.property"
    _description="Sample model"
    
    name=fields.Char(required=True)
    description=fields.Text('description')
    postcode=fields.Char()
    date_availability=fields.Date( copy=False, default= (datetime.today() + relativedelta(months=3)).date())    
    expected_price=fields.Float(required=True)
    selling_price=fields.Float(readonly=True,copy=False)
    bedrooms=fields.Integer()
    living_area=fields.Integer()
    facades=fields.Integer()
    garage=fields.Boolean()
    garden=fields.Boolean()
    garden_area=fields.Integer()
    garden_orientation=fields.Selection(
        selection=[('north','NORTH')]
    )
    active=fields.Boolean(default=True)
    property_type_id=fields.Many2one('estate.property.type', ondelete='restrict')
    salesman_id=fields.Many2one('res.users', ondelete='restrict',default=lambda self: self.env.user)
    buyer_id=fields.Many2one('res.partner', ondelete='restrict',copy=False)
    tag_ids=fields.Many2many('estate.property.tags', ondelete='restrict')
    offer_ids=fields.One2many(comodel_name='estate.property.offer', inverse_name='property_id', ondelete='cascade')