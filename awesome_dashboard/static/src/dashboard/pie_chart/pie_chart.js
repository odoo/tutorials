/** @odoo-module **/

import { Component, onWillStart, useEffect, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
	static template = "awesome_dashboard.pie_chart";
	static props = ["datasets", "labels"];

	setup() {
		this.chartContext = useRef("chartContext");
		this.chart = null;
		onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));
		useEffect(() => {
			this.renderChart();
			return () => {
				if (this.chart) this.chart.destroy();
			};
		});
	}

	renderChart() {
		if (!this.chartContext.el) return;
		if (this.chart) this.chart.destroy();

		this.chart = new Chart(this.chartContext.el, {
			type: "pie",
			data: this.props,
		});
	}
}
