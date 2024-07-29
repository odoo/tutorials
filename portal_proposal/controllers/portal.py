from odoo import http
from odoo.http import request


class ProposalPortalController(http.Controller):

    @http.route(['/my/proposals'], type='http', auth="user", website=True)
    def portal_my_proposals(self, **kw):
        partner_id = request.env.user.id
        proposals = request.env['sale.proposal'].sudo().search([('user_id', '=', partner_id)])
        return request.render("portal_proposal.proposal_portal_template", {'proposals': proposals})

    @http.route(['/my/proposals/<int:proposal_id>'], type='http', auth="user", website=True)
    def sale_proposal_portal(self, proposal_id):
        proposal = request.env['sale.proposal'].browse(proposal_id)
        if not proposal.exists():
            return request.render('http_routing.404')
        values = {
            'proposal': proposal,
        }
        return request.render('portal_proposal.proposal_portal_order_template', values)

    @http.route(['/my/proposals/accept/<int:proposal_id>'], type='http', auth="user", website=True)
    def accept_proposal(self, proposal_id, **kwargs):
        proposal = request.env['sale.proposal'].sudo().browse(proposal_id)
        if proposal:
            proposal.write({'state': 'confirm'})
        return request.redirect(f'/my/proposals/{proposal_id}')

    @http.route(['/my/proposals/reject/<int:proposal_id>'], type='http', auth="user", website=True)
    def reject_proposal(self, proposal_id, **kwargs):
        proposal = request.env['sale.proposal'].sudo().browse(proposal_id)
        if proposal:
            proposal.write({'state': 'rejected'})
        return request.redirect(f'/my/proposals/{proposal_id}')
