import { Component, useState } from "@odoo/owl";
import { DashboardItem } from "./dashboard_Item/dashboard_Item";
import { Layout } from "@web/search/layout";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";
import { items } from "./dashboard_items";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChartCard };

    setup() {
        this.action = useService("action");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        this.items = items;
        this.display = {
            controlPanel: {},
        };

    };
    openSettings() {
        this.action.doAction("base_setup.action_general_configuration");
    }

    openCustomerView() {
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
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
