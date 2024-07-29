from odoo import http
from odoo.http import request


class ProposalPortal(http.Controller):

    @http.route(['/my/proposals'], type='http', auth="public", website=True)
    def proposal_list(self, **kwargs):
        proposals = request.env['sale.proposal'].search([])
        return request.render('portal_proposal.portal_proposal_list', {
            'proposals': proposals
        })

    @http.route(
        ["/my/proposal/<int:proposal_id>"], type="http", auth="public", website=True
    )
    def proposal_view(self, proposal_id, **kwargs):
        proposal = request.env["sale.proposal"].sudo().browse(proposal_id)
        if not proposal.exists():
            return request.render("website.404")
        return request.render(
            "portal_proposal.portal_proposal_view", {"proposal": proposal}
        )

    @http.route(
        ["/my/proposal/reject/<int:proposal_id>"],
        type="http",
        auth="user",
        website=True,
    )
    def reject_proposal(self, proposal_id, **kw):
        proposal = request.env["sale.proposal"].browse(proposal_id)
        if proposal:
            proposal.write({"proposal_status": "rejected"})
        return request.redirect("/my/proposal/%d" % proposal_id)

    @http.route('/my/proposal/update', type='http', auth="public", methods=['POST'], website=True)
    def update_proposal(self, **kwargs):
        proposal_id = int(kwargs.get('proposal_id'))
        proposal = request.env['sale.proposal'].browse(proposal_id)

        if proposal.exists():
            for line in proposal.order_line:
                qty_key = f'quantity_{line.id}'
                price_key = f'price_{line.id}'

                if qty_key in kwargs and price_key in kwargs:
                    line.write({
                        'product_uom_qty': float(kwargs[qty_key]),
                        'price_unit': float(kwargs[price_key]),
                    })

        return request.redirect(f'/my/proposal/{proposal.id}')

    @http.route(['/my/proposal/accept/<int:proposal_id>'], type='http', auth="public", website=True)
    def proposal_accept(self, proposal_id, **post):
        proposal = request.env['sale.proposal'].sudo().browse(proposal_id)
        if proposal.exists() and proposal.state == 'sent':
            proposal.action_accept()
        return request.redirect('/my/proposal/%s' % proposal_id)
