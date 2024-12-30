import { Component, onWillStart, useEffect } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        orders: Object
    }

    setup() {
        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        useEffect(() => {
            const chartElt = document.getElementById("orders_chart");
            this.chart = new Chart(chartElt, {
                type: 'pie',
                data: {
                    labels: ["m", "s", "xl"],
                    datasets: [{
                        data: [this.props.orders["m"], this.props.orders["s"], this.props.orders["xl"]]
                    },
                    ]
                },
            });

            return () => {
                if (this.chart) this.chart.destroy();
            }
        },
            () => [this.props.orders]
        );
    }
}
