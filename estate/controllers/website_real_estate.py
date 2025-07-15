from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from psycopg2 import IntegrityError


class EstateWebsite(http.Controller):

    # route for propwerty list with pagination and property details
    @http.route(['/properties', '/properties/<int:property_id>', '/properties/page/<int:page>'], type='http', methods=['GET'], auth='public', website=True, csrf=False)
    def list_properties(self, property_id=None, page=1, **kargs):
        # if property_id found then render property details
        if property_id:
            property = request.env['estate.property'].browse(property_id)
            return request.render('estate.property_detail_template', {'property': property})

        # if property_id not found then render all property list
        page_size = 6
        offset = (int(page) - 1) * page_size  # offset == index of properties array to start fatching
        properties = request.env['estate.property'].search([('state', 'in', ('new', 'offer_received'))], limit=page_size, offset=offset)
        total_properties = request.env['estate.property'].search_count([('state', 'in', ('new', 'offer_received'))])

        pager = request.website.pager(
            url="/properties",
            total=total_properties,
            page=page,
            step=page_size
        )
        return request.render('estate.property_list_template', {'properties': properties, 'pager': pager})

    # if route type get then render from and if post then crete offer and store in database (database interection)
    @http.route('/properties/<int:property_id>/make-offer', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def make_offer(self, property_id, **body):
        property = request.env['estate.property'].browse(property_id)

        if not property.exists():
            return request.redirect('/properties')
        try:
            request.env['estate.property.offer'].create({
                'property_id': property_id,
                'partner_id': request.env.user.partner_id.id,
                'price': float(body.get('offer_price')),
                'date_deadline': body.get('date_validity'),
            })
            return request.redirect(f'/properties/{property_id}?success=1')

        except IntegrityError:
            request.cr.rollback()  # Rollback the transaction to avoid database lock
            return request.render('estate.property_detail_template', {
                'property': property,
                'error_message': "Invalid input: Please check your offer details.",
            })

        # for sql constraits
        except ValidationError as e:
            # If there's a ValidationError from SQL constraints, show it in the template
            return request.render('estate.property_detail_template', {
                'property': property,
                'error_message': str(e),
            })

        # for usserError: current price is less than existing
        except UserError as e:
            return request.render('estate.property_detail_template', {
                'property': property,
                'error_message': str(e)
            })
