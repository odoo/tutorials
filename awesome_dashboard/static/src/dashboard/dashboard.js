import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { ConfigDialog } from "./config_dialog/config_dialog";
import "./dashboard_items";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.action = useService("action");
        this.dialog = useService("dialog");
        this.user = useService("user");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        this.display = {
            controlPanel: {},
        };
        this.items = registry.category("awesome_dashboard").getEntries().map(([id, item]) => ({ id, ...item }));
    }

    get visibleItems() {
        const disabledItems = this.getDisabledItems();
        return this.items.filter((item) => !disabledItems.includes(item.id));
    }

    getDisabledItems() {
        return this.user.settings?.awesome_dashboard_disabled_items || [];
    }

    openConfiguration() {
        this.dialog.add(ConfigDialog, {});
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
