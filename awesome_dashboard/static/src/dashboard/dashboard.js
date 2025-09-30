import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item";
import { ConfigurationDialog } from "./configuration_dialog/configuration_dialog";
import { user } from "@web/core/user";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.action = useService("action");
        this.statistics = useState(useService("statistics_service"));
        this.items = registry.category("awesome_dashboard").getAll();
        this.dialog = useService("dialog");
        this.state = useState({ disabledItems: this.getDisabledItems() })
    }

    getDisabledItems() {
        const disabled_items = user.settings.disabled_dashboard_items;
        return disabled_items ? disabled_items.split(",") : [];
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
        this.state.disabledItems = newDisabledItems;
        user.setUserSettings("disabled_dashboard_items", this.state.disabledItems.join(","));
    }

    openConfig() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            onUpdateConfig: this.updateConfig.bind(this),
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
