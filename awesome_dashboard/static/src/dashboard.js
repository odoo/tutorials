
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";

import { Component, useState, onWillStart } from "@odoo/owl";

import { DashboardItem } from "./item/dashboardItem";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.action = useService("action");
        this.state = useState({
            average_quantity : 0,
            average_time : 0,
            nb_cancelled_orders : 0,
            nb_new_orders : 0,
            total_amount : 0,
        });

        onWillStart(async () => {
            const result = await rpc("/awesome_dashboard/statistics");
            this.state.average_quantity = result.average_quantity;
            this.state.average_time = result.average_time;
            this.state.nb_cancelled_orders = result.nb_cancelled_orders;
            this.state.nb_new_orders = result.nb_new_orders;
            this.state.total_amount = result.total_amount;
        });
   
    }

    customerButtonClick() {
        this.action.doAction("base.action_partner_form");
    }

    leadsButtonClick() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('action_partner_form'),
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
            search_view_id: [false],
            domain: [],
        });
    }
    
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
