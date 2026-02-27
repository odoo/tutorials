import { Component, useState } from "@odoo/owl";
import { browser } from "@web/core/browser/browser";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { Dialog } from "@web/core/dialog/dialog";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboard_item/dashboard_item";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.action = useService("action");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        this.items = registry.category("awesome_dashboard").getAll();
        this.display = {
            controlPanel: {},
        };
        this.dialog = useService("dialog");
        this.state = useState({
            disabledItems: browser.localStorage.getItem("disabledDashboardItems")?.split(",") || []
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: 'crm.lead',
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }

    openConfiguration() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            onUpdateConfiguration: this.updateConfiguration.bind(this),
        })
    }

    updateConfiguration(newDisabledItems) {
        this.state.disabledItems = newDisabledItems;
    }
}

class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox };
    static props = ["close", "items", "disabledItems", "onUpdateConfiguration"];

    setup() {
        this.items = useState(this.props.items.map((item) => (
            { ...item, enabled: !this.props.disabledItems.includes(item.id) }
        )));
    }

    toggleCheckbox(checked, toggledItem) {
        toggledItem.enabled = checked;
        const newDisabledItems = Object.values(this.items).filter(
            (item) => !item.enabled
        ).map((item) => item.id);

        browser.localStorage.setItem("disabledDashboardItems", newDisabledItems);
        this.props.onUpdateConfiguration(newDisabledItems);
    }

    done() {
        this.props.close();
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
