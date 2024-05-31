/** @odoo-module **/

import {Component, useState} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {Layout} from "@web/search/layout";
import {Dialog} from "@web/core/dialog/dialog";
import {CheckBox} from "@web/core/checkbox/checkbox";
import {useService} from "@web/core/utils/hooks";
import {_t} from "@web/core/l10n/translation";
import {DashboardItem} from "./dashboard_item/dashboard_item";
import {useStatistics} from "./statistics/statistics";
import {browser} from "@web/core/browser/browser";

export class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout, DashboardItem};

    setup() {
        this.action = useService("action");
        this.dialog = useService("dialog");
        this.statistics = useStatistics();
        this.items = registry.category("awesome_dashboard").getAll();
        this.state = useState({
            disabledItems: browser.localStorage.getItem("disabledDashboardItems")?.split(',') || [],
        });
    }

    updateConfiguration(disabledItems) {
        this.state.disabledItems = disabledItems;
    }

    onClickOpenConfiguration() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            onUpdateConfiguration: this.updateConfiguration.bind(this),
        });
    }

    onClickOpenCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    onClickOpenLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('Leads'),
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
            search_view_id: [false],
            // domain: [['journal_id', '=', this.props.record.resId], ['activity_ids', '!=', false]],
        });
    }
}

class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = {Dialog, CheckBox};
    static props = {
        items: {type: Array},
        disabledItems: {type: Array},
        close: {type: Function},
        onUpdateConfiguration: {type: Function},
    }

    setup() {
        this.items = this.props.items.map((item) => ({
            ...item,
            enabled: !this.props.disabledItems.includes(item.id),
        }));
    }

    done() {
        this.props.close();
    }

    onChange(checked, item) {
        item.enabled = checked;
        const newDisabledItems = Object.values(this.items).filter(item => !item.enabled).map(item => item.id);
        browser.localStorage.setItem("disabledDashboardItems", newDisabledItems);

        this.props.onUpdateConfiguration(newDisabledItems);
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
