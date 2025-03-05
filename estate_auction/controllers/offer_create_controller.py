from odoo.http import Controller, request, route

class EstatePropertyOffer(Controller):
    
    @route("/estate/property/offer/create", type="http", auth="user", website=True, methods=["POST"])
    def create_offer(self, **post):
        try:
            offer_price = float(post.get("offer_price"))
            partner_id = int(post.get("partner_id"))
            property_id = int(post.get("property_id"))
        except ValueError:
            return request.redirect(f"/estate/property/{property_id}?error=Invalid Data Format")
        
        Property = request.env["estate.property"].sudo().browse(property_id)
        Partner = request.env["res.partner"].sudo().browse(partner_id)
        
        if not Property.exists() or not Partner.exists():
            return request.redirect(f"/estate/property/{property_id}?error=Invalid Property or Partner")
        
        try:
            request.env["estate.property.offer"].sudo().create({
                "partner_id": partner_id,
                "property_id": property_id,
                "price": offer_price,
            })
            return request.render("estate_auction.template_property_offer_success", {"property": Property.name})
        except Exception as e:
            return request.redirect(f"/estate/property/{property_id}?error={str(e)}")
