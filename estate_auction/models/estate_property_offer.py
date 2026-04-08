from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _inherit = "estate.property.offer"

    is_auction_bid = fields.Boolean(default=False, readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get("property_id")
            if not property_id:
                continue

            property_obj = self.env["estate.property"].browse(property_id)
            if property_obj.sale_type == "auction":
                vals["is_auction_bid"] = True
                if property_obj.state != "auction":
                    raise ValidationError(_("Cannot add bids unless the auction is active."))
                if property_obj.auction_end_time and property_obj.auction_end_time <= fields.Datetime.now():
                    raise ValidationError(_("Cannot add bids to an auction that has already ended."))
            else:
                vals["is_auction_bid"] = False

        offers = super().create(vals_list)
        auction_properties = offers.filtered("is_auction_bid").mapped("property_id")
        if auction_properties:
            auction_properties.write({'state': 'auction'})
        return offers

    def action_accept(self):
        running_auction_offers = self.filtered_domain([
            ('property_id.sale_type', '=', "auction"),
            ('property_id.state', '=', "auction"),
            ('property_id.auction_end_time', '>', fields.Datetime.now()),
        ])
        if running_auction_offers:
            raise ValidationError(_("You cannot manually accept offers while the auction is running."))

        result = super().action_accept()
        accepted_auction_bids = self.filtered_domain([
            ('property_id.sale_type', '=', "auction"),
            ('is_auction_bid', '=', True),
            ('status', '=', "accepted"),
        ])
        winner_template = self.env.ref('estate_auction.estate_auction_winner_email_template')
        for offer in accepted_auction_bids:
            if offer.partner_id:
                winner_template.send_mail(offer.id)
        return result

    def action_refuse(self):
        running_auction_offers = self.filtered_domain([
            ('property_id.sale_type', '=', "auction"),
            ('property_id.state', '=', "auction"),
            ('property_id.auction_end_time', '>', fields.Datetime.now()),
        ])
        if running_auction_offers:
            raise ValidationError(_("You cannot manually refuse offers while the auction is running."))

        newly_refused_auction_bids = self.filtered_domain([
            ('property_id.sale_type', '=', "auction"),
            ('is_auction_bid', '=', True),
            ('status', '!=', "refused"),
        ])

        result = super().action_refuse()

        for record in newly_refused_auction_bids:
            record.property_id.message_post(
                body=_(
                    "Auction bid from %(partner)s (%(price)s) was refused.",
                    partner=record.partner_id.name,
                    price=record.price,
                ),
            )
        refused_template = self.env.ref('estate_auction.estate_auction_refused_email_template')
        for offer in newly_refused_auction_bids:
            if offer.partner_id:
                refused_template.send_mail(offer.id)
        return result
