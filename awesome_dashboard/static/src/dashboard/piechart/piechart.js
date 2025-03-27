import { Component, onMounted, useState, onWillRender } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = 'piechart.piechart';
    static props = {
        data: {type: 'Object',},
    };

    setup() {
        this.state = useState({data: null});

        this.chart = null;

        this.render = async () => {
            
            this.context = document.getElementById('piechart');
            if (this.context == null || this.context == undefined) {
                return;
            }

            if (this.chart) {
                this.chart.destroy();
            }

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

            
            this.chart = new Chart(this.context, config);

        }

        onWillRender(() => {
            this.render();
        });

        onMounted(() => {
            this.render();
        });


    }
}
