/** @odoo-module **/

import { NumberCard } from "./number_card/number_card";
import { PieChart } from "./pie_chart/pie_chart";
import { registry } from "@web/core/registry";

const items = [
	{
		id: "nb_new_orders",
		description: "Number of new orders this month",
		Component: NumberCard,
		props: (data) => ({
			title: "Number of new orders this month",
			value: data.nb_new_orders,
		}),
	},
	{
		id: "total_amount",
		description: "Total amount of new orders this month",
		Component: NumberCard,
		props: (data) => ({
			title: "Total amount of new orders this month",
			value: data.total_amount,
		}),
	},
	{
		id: "average_quantity",
		description: "Average amount of t-shirt",
		Component: NumberCard,
		props: (data) => ({
			title: "Average amount of t-shirt by order this month",
			value: data.average_quantity,
		}),
	},
	{
		id: "nb_cancelled_orders",
		description: "Number of cancelled orders this month",
		Component: NumberCard,
		props: (data) => ({
			title: "Number of cancelled orders this month",
			value: data.nb_cancelled_orders,
		}),
	},
	{
		id: "average_time",
		description:
			"Average time for an order to go from 'new' to 'sent' or 'cancelled'",
		Component: NumberCard,
		size: 2,
		props: (data) => ({
			title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
			value: data.average_time,
		}),
	},
	{
		id: "orders_by_size",
		description: "Orders pie chart",
		Component: PieChart,
		props: (data) => ({
			datasets: [{ data: Object.values(data.orders_by_size) }],
			labels: Object.keys(data.orders_by_size).map((label) =>
				label.toUpperCase()
			),
		}),
	},
];

items.forEach((item) => {
	registry.category("awesome_dashboard").add(item.id, item);
});
