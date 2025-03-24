import { Component, onWillStart, useRef, onMounted } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = 'piechart.piechart';
    static props = {
        data: {type: 'Object',},
    };

    setup() {
        onMounted(async () => {
            const chartJS = await loadJS("/web/static/lib/Chart/Chart.js");

            const config = {
                type: 'pie',
                data: {
                    labels: Object.keys(this.props.data),
                    datasets: [
                        {
                            label: 'ds1',
                            data: Object.values(this.props.data),
                        }
                    ],
                },
                options: {
                    responsive: true,
                },
            };

            
            new Chart(document.getElementById('piechart'), config);
        });

    }
}
