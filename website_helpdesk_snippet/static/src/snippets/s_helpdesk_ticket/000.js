
/** @odoo-module */
import { renderToElement } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
// import { rpc } from "@web/core/network/rpc";

publicWidget.registry.get_product_tab = publicWidget.Widget.extend({
    selector: '.categories_section',
    disabledInEditableMode: false,

    init(){
        this._super(...arguments);
        this.orm = this.bindService('orm'); 
        this.customDomain = [];
    },

    async willStart(){
        if(this.el.dataset.helpdeskTeamId) {
            const helpdesk_id = parseInt(this.el.dataset.helpdeskTeamId);
            this.customDomain = [['team_id', '=', helpdesk_id]];
        }

        const result = await this.orm.searchRead(
            'helpdesk.ticket',
            this.customDomain,
            ['name', 'user_id','partner_id','priority'],
        )

        if (result && result.length) {
            const rendered = await renderToElement('website_helpdesk_snippet.category_data', {
                result,
            });
            this.el.replaceChildren(rendered);
        }
    },  
});
