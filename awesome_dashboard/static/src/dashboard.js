import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./DashboardItem/dashboardItem";
import { PieChart } from "./PieChart/pieChart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    static components = { Layout, DashboardItem, PieChart }

    setup() {
        this.action = useService("action");
        this.statistics = useService("statistics");

        onWillStart(async () => {
            this.result = await this.statistics.callrpc();
        });
    }

    viewCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    createLead() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'form']],
        });
    }


}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
