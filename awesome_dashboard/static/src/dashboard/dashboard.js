import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item";
import { ConfigurationDialog } from "./configuration_dialog/configuration_dialog";
import { browser } from "@web/core/browser/browser";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.action = useService("action");
        this.statistics = useState(useService("statistics_service"));
        this.items = registry.category("awesome_dashboard").getAll();
        this.dialog = useService("dialog");
        this.disabledItems = useState(
            { values: browser.localStorage.getItem("disabledDashboardItems")?.split(",") || [] }
        );
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: "Leads",
            target: 'current',
            res_model: 'crm.lead',
            views: [
                [false, 'list'],
                [false, 'form'],
            ],
        });
    }

    updateConfig(newDisabledItems) {
        this.disabledItems.values = newDisabledItems;
        browser.localStorage.setItem("disabledDashboardItems", newDisabledItems);
    }

    openConfig() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
            disabledItems: this.disabledItems.values,
            onUpdateConfig: this.updateConfig.bind(this),
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
