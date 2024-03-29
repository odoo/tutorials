/** @odoo-module **/

import { Component, xml } from "@odoo/owl";

// import { Layout } from "@web/search/layout";
// import { registry } from "@web/core/registry";
// import { useService} from "@web/core/utils/hooks";
// import { _t } from  "@web/core/l10n/translation";

export class DashboardItem extends Component {
	static template = "awesome_dashboard.DashboardItem";
	static defaultProps = { size : 1 };
	static props = {
		size: {type: Number, optional: true},
		slots: {type: Object, shape: {default: true}},
	};
}
