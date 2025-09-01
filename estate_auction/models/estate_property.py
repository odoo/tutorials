from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit="estate.property"
    
    sale_mode = fields.Selection([("regular", "Regular"), ("auction", "Auction")], default="regular")
    auction_state = fields.Selection([("template", "Template"), ("auction", "Auction"), ("sold", "Sold")], default="template")
    auction_end_time = fields.Datetime(string="End Time")
    auction_highest_offer = fields.Float(string="Highest Offer", readonly=True, compute="_compute_best_bid", store=True)
    auction_highest_bidder = fields.Many2one(string="Highest Bidder", comodel_name="res.partner", readonly=True, compute="_compute_best_bid", store=True)

    @api.depends("offer_ids")
    def _compute_best_bid(self):
        for record in self:
            if not record.sale_mode == "auction" or not record.offer_ids:
                record.auction_highest_offer = 0.0
                record.auction_highest_bidder = False
                continue;
            
            best_bid = max(record.offer_ids, key=lambda offer: offer.price)
            record.auction_highest_offer = best_bid[0].price
            record.auction_highest_bidder = best_bid[0].partner_id

    def _cron_check_auction_status(self):
        auction_properties = self.search([("sale_mode", "=", "auction"), ("auction_state", "=", "auction")])

        for record in auction_properties:
            if fields.Datetime.now() >= record.auction_end_time:
                record.action_end_auction()

    def action_start_auction(self):
        if not self.auction_end_time:
            raise UserError("Cannot start auction without an end date")
        
        self.auction_state = "auction"

    def action_end_auction(self):
        if self.offer_ids:
            email_template = self.env.ref("estate_auction.email_template_property_offer_notification")
            
            best_bid = max(self.offer_ids, key=lambda offer: offer.price)
            best_bid.status="accepted"

            email_template.with_context(
                message=f"Your offer of {best_bid.price} has been accepted. We will contact you soon."
            ).send_mail(best_bid.id)
            
            remaining_offers = self.offer_ids.filtered(lambda offer: offer != best_bid)
            if remaining_offers:
                remaining_offers.write({"status": "refused"})
                
                for refused_offer in remaining_offers:
                    email_template.with_context(
                        message=f"Your offer of {refused_offer.price} has been refused."
                    ).send_mail(refused_offer.id)

        self.auction_state = "sold"
        self.state = "offer_accepted"
        self.action_mark_property_sold();
    
    def action_open_invoice(self):
        if not self.invoice_id:
            return False

        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "res_id": self.invoice_id.id,
            "view_mode": "form",
            "view_id": self.env.ref("account.view_move_form").id,
            "target": "current"
        }
