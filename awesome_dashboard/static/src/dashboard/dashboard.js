import { Component, onWillStart, reactive, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";
import { ConfigurationDialog } from "./configuration_dialog/configuration_dialog";
import dashboard_items from "./dashboard_items";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { DashboardItem, Layout, PieChart };

    setup() {
        this.action = useService("action");
        this.state = reactive({ statistics: useService("statistics") });
        this.items = registry.category("awesome_dashboard").getAll();
        this.dialog = useService("dialog");
        this.context = useState({ enabled_items: this.getEnabledItems() });
    }

    getEnabledItems() {
        // Open all items by default
        const stored_items = JSON.parse(
            localStorage.getItem("enabled_items")
        );
        if (!stored_items) {
            const all_items = this.items.map((item) => item.id);
            this.setEnabledItems(all_items);
            return all_items;
        }
        return stored_items || [];
    }

    setEnabledItems(values) {
        localStorage.setItem("enabled_items", JSON.stringify(values));
        this.context.enabled_items = values;
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

    openConfiguration() {
        this.dialog.add(
            ConfigurationDialog,
            {
                items: this.items,
                enabled_items: this.context.enabled_items,
                setEnabledItems: this.setEnabledItems.bind(this),
            },
        );
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
