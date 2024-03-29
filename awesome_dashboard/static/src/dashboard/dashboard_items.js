/** @odoo-module **/

import { Component, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";

import { DashboardItem } from "./dashboard_item";
import { PieChart } from "./pie_chart";

export class NumberCard extends Component {
	static template = xml`
					<p><t t-esc="props.title"/>:</p>
					<div style="color:green;text-align:center;text-bold;font-size:30px">
						<b><t t-esc="props.value"/></b>
					</div>
					`;

	static props = {
		title: String,
		value: Number,
	}
}

export class PieChartCard extends Component {
	static template = xml`<PieChart data="props.value"/>`
	static components = { PieChart };

	static props = {
		title: String,
		value: {type: Object, values: Number},
	}
}

let items = [
	{
   id: "average_quantity",
   description: _t("Average amount of t-shirt"),
   Component: NumberCard,
   size: 3,
   props: (data) => ({
      title: _t("Average amount of t-shirt by order this month"),
      value: data.average_quantity,
   }),
	},

	{
   id: "average_time",
   description: _t("Average order processing time"),
   Component: NumberCard,
   size: 3,
   props: (data) => ({
      title: _t("Average time for an order to go from 'new' to 'sent' or 'canceled'"),
      value: data.average_time,
   }),
	},

	{
   id: "nb_new_orders",
   description: _t("Number of new orders"),
   Component: NumberCard,
   size: 3,
   props: (data) => ({
      title: _t("Number of new orders this month"),
      value: data.nb_new_orders,
   }),
	},

	{
   id: "nb_cancelled_orders",
   description: _t("Number of canceled orders"),
   Component: NumberCard,
   size: 3,
   props: (data) => ({
      title: _t("Number of cancelled orders this month"),
      value: data.nb_cancelled_orders,
   }),
	},

	{
   id: "total_amount",
   description: _t("Total amount of orders"),
   Component: NumberCard,
   size: 3,
   props: (data) => ({
      title: _t("Total amount of new orders this month"),
      value: data.total_amount,
   }),
	},

	{
   id: "orders_by_size",
   description: _t("Orders by size"),
   Component: PieChartCard,
   size: 1,
   props: (data) => ({
      title: _t("Orbders by size this month"),
      value: data.orders_by_size,
   }),
	},
];

for (let item of items) {
	registry.category("awesome_dashboard").add(item.id, item);
}

