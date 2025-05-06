/** @odoo-module */
import { renderToElement } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";


publicWidget.registry.GetHelpdeskTickets = publicWidget.Widget.extend({
    selector : ".s_helpdesk_tickets",
    disabledInEditableMode: false,
    
    init() {
        this._super(...arguments);
        this.orm = this.bindService("orm");
    },

    async willStart() {
        const helpdesk_team_id = this.el.dataset.helpdeskTeamId
        const domain = []
        if(helpdesk_team_id && helpdesk_team_id != "")
            domain.push(["team_id", "=", parseInt(helpdesk_team_id)])
        this.result = await this.orm.searchRead(
            "helpdesk.ticket",
            domain,
            ["id", "name", "user_id", "partner_id", "priority"],
        )
    },
    start() {
        if(this.result){
            this.el.innerHTML = "";
            this.el.append(renderToElement(this.el.dataset.layout == "list"? "website_helpdesk_tickets.s_helpdesk_tickets_list": "website_helpdesk_tickets.s_helpdesk_tickets_card", {result: this.result}))
        }
    },
});
