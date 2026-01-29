import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item"
import { PieChart } from "./pie_chart/pie_chart"
import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";
// import { rpc } from "@web/core/network/rpc";
import { items } from "./dashboard_items";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart, NumberCard, PieChartCard };

    setup() {
        this.action = useService("action");
        this.statsService = useService("awesome_dashboard.statistics");
        onWillStart(async () => {
            this.stats = await this.statsService.loadStatistics();
        })
        this.items = items;
    }

    openCustomerView(){
        this.action.doAction("base.action_partner_form");
    }

    openLeads(){
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Journal Entry',
            res_model: 'account.move',
            views: [[false, 'kanban']],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
