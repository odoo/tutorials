/** @odoo-module **/

import { Component, useState, onWillStart} from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { PieChart } from "./piechart/piechart";
import { DashboardItem } from "./dashboarditem/dashboarditem";
import { PieChartCard } from "./piechartcard/piechartcard";
import { NumberCard } from "./numbercard/numbercard";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";
import { rpc } from "@web/core/network/rpc";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem ,PieChart,PieChartCard,NumberCard};

    setup() {
        const dashboardItemsRegistry = registry.category("awesome_dashboard");
        this.items = dashboardItemsRegistry.getAll();
        this.action = useService("action");
        this.statistics = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.statistics.stats);
        this.dialog = useService("dialog");
        this.dialog_state = useState({
            disabledItems: [],
            isLoading: true,
        });
        onWillStart(async () => {
            try {
                const fetchedDisabledItems = await rpc("/web/dataset/call_kw/res.users/get_dashboard_settings", {
                    model: 'res.users',
                    method: 'get_dashboard_settings',
                    args: [],
                    kwargs: {},
                });
                this.dialog_state.disabledItems = fetchedDisabledItems;
            } catch (error) {
                console.error("Error loading initial dashboard settings from server:", error);
                this.dialog_state.disabledItems = [];
            } finally {
                this.dialog_state.isLoading = false;
            }
        });
    }

    openCustomers(){
        this.action.doAction("base.action_partner_form");
    }
    async openLeads(){
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
            target: "current",
        });
    }
    updateConfiguration(newDisabledItems) {
        this.dialog_state.disabledItems = newDisabledItems;
    }

    openSetting() {
        this.action.doAction("base_setup.action_general_configuration");
    }
    openConfiguration() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
            disabledItems: this.dialog_state.disabledItems,
            onUpdateConfiguration: this.updateConfiguration.bind(this),
        })
    }
}

class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox };
    static props = ["close", "items", "disabledItems", "onUpdateConfiguration"];

    setup() {
        this.items = useState(this.props.items.map((item) => {
            return {
                ...item,
                enabled: !this.props.disabledItems.includes(item.id),
            }
        }))
    }

    onDone() {
        this.props.close()
    }

    onChange(checked, changedItem) {
        changedItem.enabled = checked;
        const newDisabledItems = Object.values(this.items).filter(
            (item) => !item.enabled
        ).map((item) => item.id)

        browser.localStorage.setItem(
            "disabledDashboardItems",
            newDisabledItems,
        );
        this.props.onUpdateConfiguration(newDisabledItems);
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
