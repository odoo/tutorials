import {Component, onWillStart, useState, reactive} from "@odoo/owl";
import {_t} from "@web/core/l10n/translation";

import {registry} from "@web/core/registry";
import {Layout} from "@web/search/layout";
import {useService} from "@web/core/utils/hooks";
import {DashboardItem} from "./DashboardItem";
import {items} from "./dashboard_items"

//     "result": {
//         "average_quantity": 7,
//         "average_time": 6,
//         "nb_cancelled_orders": 6,
//         "nb_new_orders": 174,
//         "orders_by_size": {
//             "m": 14,
//             "s": 4,
//             "xl": 118
//         },
//         "total_amount": 117
//     }


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout, DashboardItem};

    static props = {
        'actionId': true,
        'action': true,
        'updateActionState': true,
        'className': true,
    };


    setup() {
        this.action = useService("action");
        this.stats_service = useService("awesome_owl.statistics");

        // Don't works
        // this.stats_service = useService("awesome_owl.statistics");
        // this.stats = useState(this.stats_service.resp);
        // this.stats = reactive(this.stats_service.resp);
        this.items = registry.category("awesome_dashboard.items").getAll();
        console.log(this.items)
    }

    openCustomer() {
        this.action.doAction("base.action_partner_form");
    }

    async openLeads(activity) {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Leads'),
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
