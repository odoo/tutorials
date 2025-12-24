import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout"
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_tem";
import { PieChartCard } from "./pie_chart/pie_chart_card";
import { NumberCard } from "./number_card/number_card";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChartCard, NumberCard };

    setup() {
        this.action = useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics")
        this.state = useState(this.statisticsService.state)
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form")
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads Entries",
            target: "current",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]]
        })
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard)
