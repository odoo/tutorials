import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";

import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { DashboardItem, Layout, PieChart };

    setup() {
        this.action = useService("action");
        this.state = {
            numOrders: 0,
            newOrders: 0,
            tShirtByOrder: 0,
            cancelledOrders: 0,
            timeFromNew: 0,
            ordersBySize: { labels: [], values: [] },
        }
        this.statistics = useService("awesome_dashboard.statistics");
        onWillStart(async () => {
            const loadedStatistics = await this.statistics.loadStatistics();
            this.state.numOrders = loadedStatistics.numOrders;
            this.state.newOrders = loadedStatistics.newOrders;
            this.state.tShirtByOrder = loadedStatistics.tShirtByOrder;
            this.state.cancelledOrders = loadedStatistics.cancelledOrders;
            this.state.timeFromNew = loadedStatistics.timeFromNew;
            this.state.ordersBySize.labels = loadedStatistics.sizeLabels;
            this.state.ordersBySize.values = loadedStatistics.sizeValues;
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "crm.lead",
            target: "current",
            views: [[false, "list"], [false, "form"]],
        })
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
