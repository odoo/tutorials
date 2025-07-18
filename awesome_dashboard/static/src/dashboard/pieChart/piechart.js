/** @odoo-module **/

import { Component, onWillStart, useRef, onMounted, useEffect, onWillUnmount } from "@odoo/owl";
import { loadJS } from "@web/core/assets"

export class PieChart extends Component {
    static template = "awesome_dashboard.Piechart";
    static props = {
        data: { type: Object },
        onSliceClick: { type: Function, optional: true },
    };
    setup() {
        this.chart = null;
        this.pieChartCanvasRef = useRef("pie_chart_canvas");

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        })

        this.chartData = {
            labels: Object.keys(this.props.data),
            datasets: [{
                data: Object.values(this.props.data)
            }]
        };

        onMounted(() => {
            this.makePieChart();
        })

        this.cleanupPieChart = () => {
            if (this.chart) {
                this.chart.destroy();
                this.chart = null;
            }
        };

        onWillUnmount(this.cleanupPieChart);

        useEffect(() => {
            this.cleanupPieChart();
            if (this.pieChartCanvasRef.el) {
                this.makePieChart();
            }
        }, () => [this.props.data])
    }

    makePieChart() {
        this.chart = new Chart(this.pieChartCanvasRef.el, {
            type: "pie",
            data: this.chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                onClick: (event, elements) => {
                    if (elements.length > 0) {
                        const clickedElementIndex = elements[0].index;
                        const label = this.chartData.labels[clickedElementIndex];
                        if (this.props.onSliceClick) {
                            this.props.onSliceClick(label);
                        }
                    }
                }
            }
        })
    }
}
