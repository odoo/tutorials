import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboard_item";
// import { rpc } from "@web/core/network/rpc" required as part of exercise.

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, rpc }
    setup() {
        this.action = useService("action");
        this.statistics = useService("awesome_dashboard.statistics");
        this.display = {
            controlPanel: {},
        };
        // onWillStart(async () => {
        //     this.statistics = await rpc("/awesome_dashboard/statistics");
        // }); was required as part of exercise

        onWillStart(async () => {
            this.statistics = await this.statistics.loadStatistics();
        }); 

    }
    openCustomer(){
        this.action.doAction("base.action_partner_form");
    }

    openLeads(){
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: "All leads",
            target: 'current',
            res_model: 'crm.lead',
            views: [
                [false, 'form'],
                [false, 'list'],
            ],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
