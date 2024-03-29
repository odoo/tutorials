/** @odoo-module **/

import { Component, onWillStart, useState, xml } from "@odoo/owl";

import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { memoize } from "@web/core/utils/functions";
import { _t } from  "@web/core/l10n/translation";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser"

import { DashboardItem } from "./dashboard_item";
import { PieChart } from "./pie_chart";
// import { items } from "./dashboard_items"

class AwesomeDashboard extends Component {
	static template = "awesome_dashboard.AwesomeDashboard";
	static components = { Layout, DashboardItem, PieChart };

	setup() {
		this.items = registry.category("awesome_dashboard").getAll();
		this.state = useState( useService("awesome_dashboard.statistics") );
		this.disabled = useState( new Set(
			browser.localStorage.getItem("disabledItems")?.split(',')
		));
		this.action = useService("action");
		this.dialog = useService("dialog");
	}

	openConf() {
		this.dialog.add(ConfigDialog, { 
			items: this.items,
			disabled: this.disabled,
		});
	}

	customersView() {
		this.action.doAction("base.action_partner_form");
	}

	leadsView() {
		this.action.doAction({
			type: "ir.actions.act_window",
			name: _t("Leads"),
			// target: "current", (point?)
			// res_id: crm_lead_all_leads_view_tree,
			// res_id: 'toto', (works also?)
			res_model: "crm.lead",
			views: [[false, "tree"], [false, "kanban"]],
		});
	}
}

class ConfigDialog extends Component {
	static template = "config_dialog";
	static props = ["close", "items", "disabled"];
	static components = { Dialog, CheckBox };

	toggleItem(enable, id) {
		if (enable) {
			this.props.disabled.delete(id);
		} else {
			this.props.disabled.add(id);
		}
	}

	done() {
		browser.localStorage
			.setItem("disabledItems", [...this.props.disabled].join(','));
		this.props.close();
	}
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
