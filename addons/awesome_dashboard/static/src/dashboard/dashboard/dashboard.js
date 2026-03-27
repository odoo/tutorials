import {Component, useState} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {Layout} from "@web/search/layout";
import {useService} from "@web/core/utils/hooks";
import {DashboardItem} from "../dashboard_item/dashboard_item";
import {PieChart} from "../charts/pie_chart/pie_chart";
import "../../dashboard_items";
import {PieChartCard} from "../charts/pie_chart_card/pie_chart_card";
import {NumberCard} from "../number_card/number_card";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout, DashboardItem, PieChart, PieChartCard, NumberCard};


    setup() {
        this.action = useService("action");
        const {statistics} = useService("awesome_dashboard.statistics");
        this.statistics = useState(statistics);
        this.items = registry.category("awesome_dashboard").getAll();
    }

    openCustomerView() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
            name: "All leads",
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
