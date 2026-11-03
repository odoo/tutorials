import { Component, usePlugin, signal, useProps } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { ActionPlugin } from "@web/webclient/actions/action_plugin";
import { DialogPlugin } from "@web/core/dialog/dialog_plugin";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { DashboardItem } from "./dashboard_item";
import { ReportingPlugin } from "./reporting_plugin";
import { PieChart } from "./pie_chart/pie_chart";
import { items } from "./dashboard_items";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart, CheckBox };

    items = items.items;

    reporting = usePlugin(ReportingPlugin);
    action = usePlugin(ActionPlugin);
    openCustomerView() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
            domain: [["type", "=", "lead"]],
        });
    }

    dialog = usePlugin(DialogPlugin);
    disabledItems = signal(
        window.localStorage.getItem("disabledDashboardItems")?.split(",") || []
    );
    updateConfiguration(newDisabledItems) {
        this.disabledItems.set(newDisabledItems);
        window.localStorage.setItem("disabledDashboardItems", newDisabledItems.join(","));
    }
    openConfiguration() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items(),
            disabledItems: this.disabledItems(),
            onUpdateConfiguration: this.updateConfiguration.bind(this),
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
registry.category("actions").add("AwesomeDashboard", AwesomeDashboard);

class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox };

    props = useProps(["close", "items", "disabledItems", "onUpdateConfiguration"]);

    disabledItems = signal(this.props.disabledItems);

    isEnabled(item) {
        return !this.disabledItems().includes(item.id);
    }

    done() {
        this.props.close();
    }

    onChange(checked, item) {
        const disabled = new Set(this.disabledItems());
        if (checked) {
            disabled.delete(item.id);
        } else {
            disabled.add(item.id);
        }
        const newDisabledItems = [...disabled];
        this.disabledItems.set(newDisabledItems);
        this.props.onUpdateConfiguration(newDisabledItems);
    }
}

registry.category("lazy_components").add("ConfigurationDialog", ConfigurationDialog);
registry.category("actions").add("ConfigurationDialog", ConfigurationDialog);
