import { Component, onWillStart, useEffect, useRef, xml } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = xml`<div><canvas t-ref="piechart"/></div>`;
    static props = {
        data: Object,
    };

    chartRef = useRef("piechart");

    setup() {
        this.chart = null;

        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));
        useEffect(
            () => {
                if (!this.chartRef.el) {
                    return;
                }
                this.chart = new Chart(this.chartRef.el, {
                    type: "pie",
                    data: {
                        labels: Object.keys(this.props.data),
                        datasets: [
                            {
                                data: Object.values(this.props.data),
                            },
                        ],
                    },
                });

                return () => {
                    if (this.chart) {
                        this.chart.destroy();
                    }
                };
            },
            () => [this.chartRef, this.props.data]
        );
    }
}
