/** @odoo-module */
import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./DashboardItem/dashboarditem"


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.dashboard";
    static components = { Layout, DashboardItem }

    setup() {
        this.display = { controlPanel: {} }
        this.action = useService("action")

        this.statistics = useState(useService("awesome_dashboard.statistics"))
        this.items = registry.category("awesome_dashboard").getAll();
    }

    customerView() {
        this.action.doAction("base.action_partner_form")
    }

    leadsView(activity) {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: ('Leads View'),
            target: 'current',
            res_id: activity.res_id,
            res_model: 'crm.lead',
            views: [[false, 'list']]
        })
    }
};

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
