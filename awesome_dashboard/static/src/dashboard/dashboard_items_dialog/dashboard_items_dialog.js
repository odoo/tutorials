/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class DashboardItemsDialog extends Component {
	static template = "awesome_dashboard.DashboardItemsDialog";
	static components = { Dialog };
	static props = {
		items: { type: Array },
		apply: Function,
		close: Function,
	};

	setup() {
		this.items = useState(this.props.items);
	}
	toggleItem(item) {
		item.isSelected = !item.isSelected;
	}
	apply() {
		this.props.apply(
			this.items.filter((e) => !e.isSelected).map((e) => e.id)
		);
		this.props.close();
	}
}
