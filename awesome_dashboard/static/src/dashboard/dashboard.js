import { Component, useRef, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { _t } from "@web/core/l10n/translation";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout, DashboardItem};

    setup() {
        this.action = useService("action");
        this.statistics = useState(useService("awesome_dashboard.statistics").loadStatistics);
        this.dialogService = useService("dialog");
        this.items = registry.category("awesome_dashboard").getAll();
        this.state = useState({
            disabledItems: localStorage.getItem("awesome_dashboard_disabled")?.split(',') || []
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window', target: 'current', res_model: 'crm.lead', views: [[false, "list"], [false, 'form'],],
        });
    }

    updateDashboard(disabledItems) {
        this.state.disabledItems = disabledItems;
    }

    openDialog() {
        this.dialog = this.dialogService.add(
            DashboardConfiguration,
            {items: this.items, disabledItems: this.state.disabledItems, doneUpdating: this.updateDashboard.bind(this)},
            {});
    }
}

class DashboardConfiguration extends Component {
    static template = "awesome_dashboard.DashboardConfiguration";
    static components = {Dialog, CheckBox, _t};
    static props = ["close", "items", "disabledItems", "doneUpdating"];


    setup() {
        this.options = useRef("options");
        this.items = useState(this.props.items.map(item => ({...item, disabled: this.props.disabledItems.includes(item.id)})));
        this.title = _t('Dashboard items configuration');
    }

    updateDisabled(item, checked) {
        item.disabled = !checked;
    }

    apply() {
        const disabledItems = this.items.filter(item => item.disabled).map(item => item.id);
        localStorage.setItem("awesome_dashboard_disabled", disabledItems);
        this.props.doneUpdating(disabledItems);
        this.props.close();
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
