import { Component, xml, useRef, onWillStart, useEffect, onWillUnmount } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = xml`<canvas t-ref="chart" width="400" height="400"></canvas>`

    static props = {
        labels: { type: Array },
        datasets: { type: Array },
    }

    setup() {
        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        })

        this.canvasRef = useRef("chart");
        this.chartInstance = null;

        useEffect(() => {
            if (!this.chartInstance) {
                    this.chartInstance = new Chart(this.canvasRef.el, {
                        type: 'pie',
                        data: {
                            labels: this.props.labels,
                            datasets: this.props.datasets
                        }
                    })
                } else {
                    this.chartInstance.data.labels = this.props.labels;
                    this.chartInstance.data.datasets[0].data = this.props.datasets[0].data;
                    this.chartInstance.update();
                }
        })

        onWillUnmount(() => {
            if (this.chartInstance) {
                this.chartInstance.destroy();
            }
        })
    }
}
