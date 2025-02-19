import { Component, onWillStart, useState } from "@odoo/owl";
import { DashboardItem } from "./dashboard_item";
import { Layout } from "@web/search/layout";
import { PieChart } from "./pie_chart/pie_chart";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        this.display = {
            controlPanel: {},
        };
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.statisticsService.statistics);
        // onWillStart(async () => {
        //     // const result = await this.statisticsService.loadStatistics();
        //     if (this.statistics.isReady){
        //         console.log(this.statistics.orders_by_size);
        //         this.statistics = [
        //             { label: "New Orders (This Month)", value: this.statistics.nb_new_orders },
        //             { label: "Total Order Amount (This Month)", value: this.statistics.total_amount },
        //             { label: "Avg T-Shirts per Order", value: this.statistics.average_quantity },
        //             { label: "Cancelled Orders", value: this.statistics.nb_cancelled_orders },
        //             { label: "Avg Time from New to Sent/Cancelled", value: this.statistics.average_time },
        //         ];
        //         this.statistics.orderBySize = this.statistics.orders_by_size;
        //     }
        // });
    }
    
    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "All leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
            target: "current",
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);