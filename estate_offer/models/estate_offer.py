from odoo import api, fields, models


class Estate(models.Model):
    _inherit = "estate.estate"

    offer_ids = fields.One2many("estate.offer", inverse_name="estate_id")


class Offer(models.Model):
    _name = "estate.offer"
    _description = "This is the offer model."

    amount = fields.Float(required=True)
    estate_id = fields.Many2one("estate.estate", required=True)

    # user_id = fields.Many2one("res.user", required=True)
