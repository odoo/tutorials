/** @odoo-module **/
import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
// import { rpc } from "@web/core/network/rpc"
import { PieChart } from "./pie_chart/pie_chart"


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, PieChart };

    setup() {
        this.myService = useService("awesome_dashboard_service");
        this.action = useService("action");
        this.statistics = useService("awesome_dashboard.statistics");

        // state for statistics cards
        this.state = useState(this.statistics);

        //rpc calls every time means reopeing dashboard refreshes value
        // onWillStart(async () => {
        //     this.state.stats = await rpc("/awesome_dashboard/statistics", {})
        // });

        //memoize means reopeing dashboard will not refreshes, value will store in cache
        // onWillStart(async () => {
        //     this.state.stats = await this.statistics.loadStatistics();
        // });

    }

    inc() {
        this.myService.inc();
        this.render(); // simple way to refresh UI for now
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"]
            ],
        });
    }
}

// registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);

