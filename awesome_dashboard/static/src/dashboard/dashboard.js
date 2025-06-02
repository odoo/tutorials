/** @odoo-module **/

import { Component, useState, onWillStart, onWillRender} from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { Piechart } from "./components/piechart/piechart";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, Piechart}
    layout_display = { controlPanel: {} } 
    
    setup() {
        this.action = useService("action");
        this.dialog = useService("dialog");
        this.statsService = useService("awesome_dashboard.dashboard_stats");
        this.data_proxy = useState(this.statsService.getDataProxy());

        onWillStart(async () => {
            this.data_proxy.data = await this.statsService.fetchNow();
        })

        this.items = registry.category("awesome_dashboard").get("dashboard_items");
        this.config = useState({
            disabledItems: browser.localStorage.getItem("AwesomeDashboard.config.disabledItems")?.split(",") || [] 
        });
    }

    openConfiguration() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
            disabledItems: this.config.disabledItems,
            onUpdateConfiguration: this.updateConfiguration.bind(this),
        })
    }

    updateConfiguration(newDisabledItems) {
        this.config.disabledItems = newDisabledItems;
    }

    isEnabled(itemId) {
        return !this.config.disabledItems.includes(itemId);
    }
    
    goToCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    goToLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t(''),
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);

class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox };
    static props = ["close", "items", "disabledItems", "onUpdateConfiguration"];

    setup() {
        // A map where the key is the id of the dashboard item, and the value is whether the item is enabled or not.
        this.item_enabled_map = useState(Object.fromEntries(
            this.props.items.map(item => [item.id, !this.props.disabledItems.includes(item.id)])
        ));        
    }

    done() {
        this.props.close();
    }

    onChange(checked, changedItem) {
        this.item_enabled_map[changedItem.id] = checked;

        const newDisabledItems = Object.values(this.props.items).filter(
            (item) => !this.item_enabled_map[item.id]
        ).map((item) => item.id);

        browser.localStorage.setItem(
            "AwesomeDashboard.config.disabledItems",
            newDisabledItems,
        );

        this.props.onUpdateConfiguration(newDisabledItems);
    }
}
