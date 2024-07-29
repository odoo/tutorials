from odoo import http
from odoo.http import request, Controller


class SalePortalController(Controller):
    @http.route(['/my/sale_proposal', '/my/sale_proposal/<int:proposal_id>'], type='http', auth="user", website=True)
    def sale_proposal_portal(self, proposal_id, **kwargs):
        proposal = request.env['sale.proposal'].browse(proposal_id)
        if not proposal.exists():
            return request.render('http_routing.404')

        values = {
            'proposal': proposal,
        }
        return request.render('sale_proposal.sale_proposal_order_portal', values)

    @http.route(['/my/sale_proposal/accept/<int:proposal_id>'], type='http', auth="user", website=True)
    def action_accept(self, proposal_id, **kwargs):
        proposal = request.env['sale.proposal'].browse(proposal_id)
        if not proposal.exists():
            return request.render('http_routing.404')

        proposal.write({
            'proposal_status': 'approved',
            'state': 'confirm',
            'sale_order': f"/my/sale_proposal/{proposal_id}"
        })

        return request.redirect(proposal.get_portal_url())

    @http.route(['/my/sale_proposal/reject/<int:proposal_id>'], type='http', auth="user", website=True)
    def action_reject(self, proposal_id, **kwargs):
        proposal = request.env['sale.proposal'].browse(proposal_id)
        if not proposal.exists():
            return request.render('http_routing.404')

        proposal.write({'proposal_status': 'rejected'})

        return request.redirect(proposal.get_portal_url())
