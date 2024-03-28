/** @odoo-module **/

import { Component, onMounted, onWillStart, useEffect, useRef, useState, xml } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
	static template = xml`<canvas t-ref="canvas_ref">pie chart</canvas>`;
	static props = { 
		data: {type: Object, values: Number},
	};

	setup() {
		let canvasRef = useRef("canvas_ref");
		onWillStart(async () => {
			await loadJS("/web/static/lib/Chart/Chart.js");
		});

// 		useEffect( 
// 			(data) => {
// 				this.chart = new Chart(canvasRef.el.getContext('2d'), {
// 					type: "pie",
// 					data: {
// 						datasets: [{ 
// 							data: Object.values(data),
// 						}],
// 						labels: Object.keys(data),
// 					},
// 				});
// 				return () => { this.chart.destroy(); };
// 			},
// 			() => [this.props.data]
// 		);
		
		onMounted( async () => {
			this.chart = new Chart(canvasRef.el.getContext('2d'), {
				type: "pie",
				data: {
					datasets: [{ 
						data: Object.values(this.props.data),
					}],
					labels: Object.keys(this.props.data),
				},
			});
		});

		useEffect( (data) => {
			this.chart.data.datasets[0].data = Object.values(data);
			this.chart.update();
		},
		() => [this.props.data]
		);
	}

// // 		let updateChart = () => {
// // 			this.chart = new Chart(canvasRef.el.getContext('2d'), {
// // 				type: "pie",
// // 				data: {
// // 					datasets: [{ 
// // 						data: Object.values(this.props.data),
// // 					}],
// // 					labels: Object.keys(this.props.data),
// // 				},
// // 			});
// // 		};
// 
// 		onMounted(async () => {
// 			this.chart = new Chart(canvasRef.el.getContext('2d'), {
// 				type: "pie",
// 				data: {
// 					datasets: [{ 
// 						data: Object.values(this.props.data),
// 					}],
// 					labels: Object.keys(this.props.data),
// 				},
// 			});
// 		});
// 		onWillPatch(async () => { 
// 			this.chart.update();
// 			this.chart.render(); 
// 		});

// 		onMounted(async () => updateChart() );
// 		onWillPatch(async () => {
// 			this.chart.destroy();
// 			updateChart();
// 		});
// 
// 	}

}
