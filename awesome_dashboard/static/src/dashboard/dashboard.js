/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { _t } from "@web/core/l10n/translation";
import { rpc } from "@web/core/network/rpc";

async function saveDisabledItems(ids) {
    await rpc("/awesome_dashboard/save_disabled_items", {
        disabled_items: JSON.stringify(ids),
    });
}

async function loadDisabledItems() {
    const res = await rpc("/awesome_dashboard/get_disabled_items");
    return JSON.parse(res);
}

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem} ;

    setup(){
        this.actions = useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics");
        this.statistics = useState(this.statisticsService.statistics);
        this.dialog = useService("dialog");
        this.display = { controlPanel: {} };
        this.items = registry.category("awesome_dashboard").getAll();
        // this.state = useState({
        //     disabledItems: browser.localStorage.getItem("disabledDashboardItems")?.split(",") || []
        // });

        this.state = useState({
            disabledItems: [],
        });

        onWillStart(async () => {
            this.state.disabledItems = await loadDisabledItems();
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
        this.state.disabledItems = newDisabledItems;   // updates UI
        saveDisabledItems(newDisabledItems);
    }


    openCustomersView(){
        this.actions.doAction("base.action_partner_form");
    }

    openAllLeads(){
        this.actions.doAction({
            type: "ir.actions.act_window",
            name: _t("All leads"),
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"]
            ]
        });
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
        }));
    }

    done() {
        this.props.close();
    }

    onChange(checked, changedItem) {
        changedItem.enabled = checked;
        const newDisabledItems = Object.values(this.items).filter(
            (item) => !item.enabled
        ).map((item) => item.id)

        this.props.onUpdateConfiguration(newDisabledItems);
    }

}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);