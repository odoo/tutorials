from odoo import models, fields


class EstateAuctionStage(models.Model):
    _name = "estate.auction.stage"
    _description = "Auction Stages"

    name = fields.Char(string="Stage Name", required=True)
    color = fields.Integer(string="Color Index")
    icon = fields.Char(string="Icon", help="Font Awesome Icon Class")
