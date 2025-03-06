from odoo import models, fields, api, _
from odoo.exceptions import UserError

class EstateAuctionStageMixin(models.AbstractModel):
    _name = "estate.auction.stage.mixin"
    _description = "Auction Stage Mixin"

    auction_stage = fields.Selection(
        [("template", "Template"), ("auction", "Auction"), ("sold", "Sold")],
        string="Auction Stage",
        default="template",
        tracking=True,
    )
    auction_stage_selection = fields.Many2one(
        "estate.auction.stage", 
        string="Auction Stage",
        default=lambda self: self.env["estate.auction.stage"].search([], limit=1)
    )

    def action_set_auction_stage(self, stage):
        """ Updates the auction stage based on selection from UI """
        stage_record = self.env["estate.auction.stage"].search([("name", "=", stage)], limit=1)
        if not stage_record:
            raise UserError(_("Invalid stage selection."))
        self.write({"auction_stage": stage, "auction_stage_selection": stage_record.id})
