
import { Component, useState } from "@odoo/owl";

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";

import { DashboardItem } from "./dashboard_item/dashboardItem";

import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";


export class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.action = useService("action");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        this.items = registry.category("awesome_dashboard").getAll();

        this.dialog = useService("dialog");
        this.state = useState({
            uncheckedItems : [],
        });
    }

    customerButtonClick() {
        this.action.doAction("base.action_partner_form");
    }

    leadsButtonClick() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('action_partner_form'),
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
            search_view_id: [false],
            domain: [],
        });
    }

    configuration() {
        this.dialog.add(DashboardConfigs, {
            items: this.items,
            disabledItems: this.state.uncheckedItems,
            applyConfig: this.applyConfiguration.bind(this),
        })
    }

    applyConfiguration(newConfig){
        this.state.uncheckedItems = newConfig;
    }
}

export class DashboardConfigs extends Component {
    static template = "awesome_dashboard.DashboardConfigs";
    static components = { Dialog, CheckBox }

    static props = {
        items: Object,
        disabledItems: Array,
        applyConfig: Function,
        close: Function,
    }

    setup() {
        this.items = useState(this.props.items.map((item) => {
            return {
                ...item,
                checked: !this.props.disabledItems.includes(item.id),
            }
        }));
    }

    apply(){
        this.props.applyConfig(this.props.disabledItems);
        this.props.close();
    }

    toggle(checked, item){
        item.checked = checked;
        if (checked) {
            this.props.disabledItems = this.props.disabledItems.filter(item.id);
        }
        else{
            this.props.disabledItems = this.props.disabledItems.concat([item.id]);
        }
    }
}


registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
