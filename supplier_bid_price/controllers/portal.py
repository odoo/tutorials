from odoo import http
from odoo.http import request


class BidController(http.Controller):

    @http.route('/update_bids', type='json', auth='user', methods=['POST'])
    def update_bids(self, bids):
        if not bids:
            return {'success': False, 'message': 'No bid data received'}

        mail_values = []
        for bid in bids:
            order_id = bid.get("order_id")
            line_id = bid.get("line_id")
            bid_qty = float(bid.get("bid_qty", 0))
            bid_price = float(bid.get("bid_price", 0))

            order = request.env['purchase.order'].browse(order_id)
            line = request.env['purchase.order.line'].browse(line_id)
            if line.exists():
                if line.bid_qty != bid_qty or line.bid_price != bid_price:
                    mail_values.append({
                        'product_id': line.product_id.sudo().name,
                        'bid_qty': bid_qty,
                        'bid_price': bid_price
                    })
                    line.write({
                        'bid_qty': bid_qty,
                        'bid_price': bid_price,
                    })
        order._send_bid_update_email(mail_values)
        return {'success': True, 'message': 'Bids updated successfully'}
