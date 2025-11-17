
// /** @odoo-module */
// import { renderToElement } from "@web/core/utils/render";
// import publicWidget from "@web/legacy/js/public/public_widget";
// // import { rpc } from "@web/core/network/rpc";

// publicWidget.registry.get_product_tab = publicWidget.Widget.extend({
//     selector: '.categories_section',
//     disabledInEditableMode: false,

//     init() {
//         this._super(...arguments);
//         this.orm = this.bindService("orm");
//         this.customDomain = [];
//         this.result = []; 
//     },

//     async willStart() {
//         const helpdeskTeamId = this.el.dataset.helpdeskTeamId;
//         if (helpdeskTeamId) {
//             this.customDomain = [["team_id", "=", parseInt(helpdeskTeamId)]];
//         }

//         this.layout = this.el.dataset.layout || "list";  

//         this.result = await this.orm.searchRead(
//             "helpdesk.ticket",
//             this.customDomain,
//             ["name", "user_id", "partner_id", "priority"]
//         );
//     },

//     start() {
//         if (this.result && this.result.length) {
//             const templateName =
//                 this.layout === "list"
//                     ? "website_helpdesk_snippet.helpdesk_ticket_list"
//                     : "website_helpdesk_snippet.helpdesk_ticket_card";

//             const rendered = renderToElement(templateName, { result: this.result });
//             this.el.replaceChildren(rendered); 
//         }
//     },
// });

/** @odoo-module **/

import { Interaction } from "@web/public/interaction";
import { registry } from "@web/core/registry";
import { renderToElement } from "@web/core/utils/render";

export class GetProductTab extends Interaction {
    static selector = ".categories_section";

    setup(){
        this.orm = this.services.orm;
    }
    
    async willStart() {
        
        const helpdeskTeamId = this.el.dataset.helpdeskTeamId;
        this.customDomain = [];
        if (helpdeskTeamId) {
            this.customDomain = [["team_id", "=", parseInt(helpdeskTeamId)]];
        }
        
        this.layout = this.el.dataset.layout || "list";
        this.result = await this.orm.searchRead(
            "helpdesk.ticket",
            this.customDomain,
            ["name", "user_id", "partner_id", "priority"]
        );
    }

    start() {
        if (this.result && this.result.length) {
            const templateName = 
                this.layout === "list"
                    ? "website_helpdesk_snippet.helpdesk_ticket_list"
                    : "website_helpdesk_snippet.helpdesk_ticket_card";

            const rendered = renderToElement(templateName, { result: this.result });
            this.el.replaceChildren(rendered);
        }
    }
}

registry
        .category("public.interactions")
        .add("website_helpdesk.get_product_tab", GetProductTab);
        
registry
        .category("public.interactions.edit")
        .add("website_helpdesk.get_product_tab", { Interaction: GetProductTab} );

