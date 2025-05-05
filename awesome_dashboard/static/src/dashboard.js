import { Component, onWillStart } from "@odoo/owl";
import { DashboardItem } from "./dashboard_item";
import { CamembertChart } from "./camembert_chart/camembert_chart";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, CamembertChart };

    setup() {
        this.action = useService("action");
        this.statistics = useService("awesome_dashboard.statistics");

        onWillStart(async () => {
            this.statistics = await this.statistics.loadStatistics();
        });
    }

    showKanbanCustomersView() {
        this.action.doAction("base.action_partner_form");
    }

    showLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
