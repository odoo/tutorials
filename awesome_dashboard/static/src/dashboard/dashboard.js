/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { Dialog } from "@web/core/dialog/dialog";
import { browser } from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    async setup() {
        this.dialog = useService("dialog");
        this.actionService = useService("action");
        this.display = {
            controlPanel: {}
        };
        this.statistics = useState(useService("awesome_dashboard.statistics"));

        this.items = registry.category("awesome_dashboard").get("items").map((i, index) => (
            { ...i, index: index }
        ));

        this.enabledItems = useState(this.items.map(
            i => JSON.parse(browser.localStorage.getItem(i.id) ?? 'true'))
        );
    }

    _openKanbanViewAllCustomers() {
        this.actionService.doAction("base.action_partner_form");
    }

    _openLeads() {
        this.actionService.doAction({
            type: 'ir.actions.act_window',
            name: _t('Leads'),
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }

    _openConfig() {
        this.dialog.add(ConfigDialog, {
            items: this.items,
            enabledItems: this.enabledItems
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);

class ConfigDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog };
    static props = {
        items: { type: Array },
        enabledItems: { type: Array },
        close: { type: Function }
    };

    setup() {
        this.configurables = useState(this.props.items.map(i => ({
            item: i,
            enabled: this.props.enabledItems[i.index]
        })));
    }

    _onCheck(index) {
        const configurable = this.configurables[index];
        if (configurable) configurable.enabled = !configurable.enabled;
    }

    _onDone() {
        this.configurables.forEach(configurable => {
            browser.localStorage.setItem(configurable.item.id, JSON.stringify(configurable.enabled));
        });
        this.props.enabledItems.splice(0, this.props.enabledItems.length, ...this.configurables.map(c => c.enabled));
        this.props.close();
    }
}