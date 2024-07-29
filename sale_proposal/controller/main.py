from odoo import http
from odoo.http import request


class SaleProposalController(http.Controller):

    @http.route(['/my/sale_proposal', '/my/sale_proposal/<int:proposal_id>'], type='http', auth="user", website=True)
    def portal_sale_proposal(self, proposal_id, **kwargs):
        proposal = request.env['sale.proposal'].browse(proposal_id)
        if not proposal.exists():
            return request.render('http_routing.404')

        values = {
            'proposal': proposal,
        }
        return request.render('sale_proposal.portal_sale_proposal_template', values)

    @http.route(['/my/sale_proposal/accept/<int:proposal_id>'], type='http', auth="user", website=True)
    def accept_proposal(self, proposal_id, **kwargs):
        proposal = request.env['sale.proposal'].sudo().browse(proposal_id)
        if proposal:
            proposal.write({'state': 'confirm'})
        return request.redirect(f'/my/sale_proposal/{proposal_id}')

    @http.route(['/my/sale_proposal/reject/<int:proposal_id>'], type='http', auth="user", website=True)
    def reject_proposal(self, proposal_id, **kwargs):
        proposal = request.env['sale.proposal'].sudo().browse(proposal_id)
        if proposal:
            proposal.write({'state': 'rejected'})
        return request.redirect(f'/my/sale_proposal/{proposal_id}')
