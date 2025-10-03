/** @odoo-module **/

import { Component, onWillStart, useState, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboard_item";
import { Dialog } from "@web/core/dialog/dialog";
import { browser } from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.items = registry.category("awesome_dashboard.dashboard_items").getAll();
        this.action = useService("action");
        this.service = useService("awesome_dashboard.statistics")
        this.state = useState(this.service.stats);
        this.dialog = useService("dialog");
        this.unselectedIds = useState({
            value: JSON.parse(browser.localStorage.getItem("dashboard_items") || "[]"),
        })
        onWillStart(async () => {
            await this.service.loadStatistics();
        });
    }

    goToCustomers() {
        this.action.doAction("base.action_partner_form")
    }

    goToLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }

    updateConfig(items) {
        this.unselectedIds.value = items;
        browser.localStorage.setItem("dashboard_items", JSON.stringify(items));
    }

    openDialog() {
        this.dialog.add(AwesomeDialog, {
            title: "Dashboard items configuration",
            description: "Which cards do you wish to see?",
            fields: this.items,
            unselectedFields: this.unselectedIds.value,
            save: this.updateConfig.bind(this),
        });
    }

}

class AwesomeDialog extends Component {
    static template = "awesome_dashboard.AwesomeDialog";
    static components = { Dialog };
    static props = {
        title: String,
        description: String,
        fields: Array,
        close: Function,
        save: Function,
        unselectedFields: Array,
    };
    setup() {
        this.checkboxes = this.props.fields.map((field) => {
            return {
                ref: useRef(field.id),
                id: field.id,
            };
        });
    }

    closeDialog() {
        const unselectedIds = this.checkboxes.filter((checkbox) => !checkbox.ref.el.checked).map((checkbox) => checkbox.id);
        this.props.save(unselectedIds);
        this.props.close();
    }

}

registry.category("lazy_components").add("Dashboard", AwesomeDashboard);
