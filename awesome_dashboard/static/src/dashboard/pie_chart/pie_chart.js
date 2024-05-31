/** @odoo-module **/
import { Component, onMounted, onWillPatch, onWillStart, onWillUnmount, useEffect, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        title: { type: String},
        data: { type: Object }
    };

    setup() {
        this.chart = null;
        this.canvasRef = useRef("canvas");

        onWillStart(() => loadJS("/web/static/lib/Chart/Chart.js"));
        useEffect(() => {
            this._renderChart();
            return () => this.chart.destroy();
        }, () => [...[this.props.data]]);
    }

    _renderChart() {
        this.chart = new Chart(
            this.canvasRef.el,
            {
                type: "pie",
                data: {
                    labels: Object.keys(this.props.data),
                    datasets: [
                        {
                            data: Object.values(this.props.data),
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Orders by Size'
                        }
                    }
                }
            }
        );
    }

}