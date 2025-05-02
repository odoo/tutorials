import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { Card } from "./card/card"
import { PieChart } from "./pie_chart/pie_chart"

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, Card, PieChart };

    setup() {
        this.display = { controlPanel: {} };
        this.action = useService("action");
        this.stats = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.stats.loadStatistics());
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            target: "current",
            res_model: "crm.lead",
            views: [[false, "list"],[false, "form"]],
        });
    }
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
