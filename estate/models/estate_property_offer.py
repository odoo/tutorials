from odoo import fields, models
 
class EstatePropertyOffer(models.Model):
    _name="estate.property.offer"
    _description="Estate property Offers"
     
    price=fields.Integer()
    status = fields.Selection(string="Status", selection=[("accepted","Accepted"),("refused","Refused")],copy=False)
    partner_id= fields.Many2one("res.partner",required=True)
    property_id= fields.Many2one("estate.property",required=True)
    active = True
