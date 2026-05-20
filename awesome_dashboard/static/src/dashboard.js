import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./DashboardItem/dashboarditem"
import { rpc } from "@web/core/network/rpc"


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem }

    setup() {
        this.display = { controlPanel: {} }
        this.action = useService("action")
        
        const statisticService = useService("awesome_dashboard.statistics")
        onWillStart(async() => {
            this.statistics = await statisticService.loadStatistics();
        })
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

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
