import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "@awesome_dashboard/dashboard-item";
import { PieChart } from "@awesome_dashboard/piechart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.display = {
            controlPanel: {},
        };
        this.statistics = useService("awesome_dashboard.statistics");
        onWillStart(async () => {
            this.statistics = await this.statistics.loadStatistics();
        });
        this.action = useService("action");
    }
    openCustomers(){
        this.action.doAction("base.action_partner_form");
    }
    openLeads(){
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "All Leads",
            res_model: "crm.lead",
            views:[
                [false,'list'],
                [false,'form'],
            ]
        })
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);