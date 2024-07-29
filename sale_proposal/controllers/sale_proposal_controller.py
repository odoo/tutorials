from odoo import http
from odoo.http import request


class SaleProposalController(http.Controller):
    @http.route('/my/sale_proposal', type='http', auth='user', website=True)
    def show_proposals(self, **kwargs):
        proposals = request.env['sale.proposal'].search([])
        values = {
            'proposals': proposals,
        }
        return request.render('sale_proposal.portal_sale_proposal_template', values)

    @http.route(['/my/sale_proposal/<int:proposal_id>'], type='http', auth="user", website=True)
    def portal_sale_proposal(self, proposal_id, **kw):
        proposal = request.env['sale.proposal'].browse(proposal_id)
        if not proposal.exists():
            return request.render('http_routing.404')
        values = {
            'proposal': proposal,
        }
        return request.render('sale_proposal.portal_sale_proposal_template', values)

    @http.route(['/my/sale_proposal/accept/<int:proposal_id>'], type='http', auth="user", website=True)
    def accept_proposal(self, proposal_id, **kw):
        proposal = request.env['sale.proposal'].browse(proposal_id)
        if proposal:
            proposal.write({'state': 'sale', 'proposal_status': 'approved'})
        return request.redirect('/my/sale_proposal/%d' % proposal_id)

    @http.route(['/my/sale_proposal/reject/<int:proposal_id>'], type='http', auth="user", website=True)
    def reject_proposal(self, proposal_id, **kw):
        proposal = request.env['sale.proposal'].browse(proposal_id)
        if proposal:
            proposal.write({'proposal_status': 'rejected'})
        return request.redirect('/my/sale_proposal/%d' % proposal_id)
