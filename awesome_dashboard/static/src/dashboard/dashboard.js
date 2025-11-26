import { Component, onWillStart, reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";
import dashboard_items from "./dashboard_items";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { DashboardItem, Layout, PieChart };

    setup() {
        this.action = useService("action");
        this.state = reactive({ statistics: useService("statistics") });
        this.items = registry.category("awesome_dashboard").getAll();
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [
                [false, 'list'],
                [false, 'form'],
            ],
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
