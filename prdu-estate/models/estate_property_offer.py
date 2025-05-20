from odoo import fields, models


class estatePropertyOffer(models.Model):
	_name="estate.property.offer"
	_description = "You receive: Northing. I receive: a goddamn house."
	price = fields.Float()
	status = fields.Selection(selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False)
	partner_id = fields.Many2one("res.partner", string="Partner", required=True)
	property_id = fields.Many2one("estate.property", required=True)
