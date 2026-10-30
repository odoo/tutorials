import { Component, signal, useProps, usePlugin } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { DialogPlugin } from "@web/core/dialog/dialog_plugin";
import { ActionPlugin } from "@web/webclient/actions/action_plugin";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { DashboardItem } from "./dashboard_item";
import { dashboardItems } from "./dashboard_items";
import { ReportingPlugin } from "./reporting_plugin";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    disabledItems = signal(
        window.localStorage.getItem("disabledDashboardItems")?.split(",") || []
    );
    action = usePlugin(ActionPlugin);
    reporting = usePlugin(ReportingPlugin);
    dialog = usePlugin(DialogPlugin);
    items = dashboardItems.items;

    openConfiguration() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items(),
            disabledItems: this.disabledItems(),
            onUpdateConfiguration: this.updateConfiguration.bind(this),
        });
    }

    updateConfiguration(newDisabledItems) {
        this.disabledItems.set(newDisabledItems);
        window.localStorage.setItem("disabledDashboardItems", newDisabledItems);
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

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
