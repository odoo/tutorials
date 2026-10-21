import {Component , onWillStart , onMounted , useRef , onPatched } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";

    static props = { data : Object };

    setup(){
        this.canvasRef = useRef("canvas");

        onWillStart(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
        });

        onMounted( () => {
            const quantities = this.props.data;

            this.chart = new Chart(this.canvasRef.el , {
                type : "pie",
                data : {
                    labels : [ "S ", "M" , "XL"],
                    datasets : [
                        {
                            data : [
                                quantities.s,
                                quantities.m,
                                quantities.xl,

                            ]
                        }
                    ]
                }

            });
        });

        onPatched(() => {
            this.updateChart();
        });
    }

    updateChart(){
        if(!this.chart || !this.props.data){
            return;
        }

        const quantities = this.props.data;
        this.chart.data.datasets[0].data = [
            quantities.s, quantities.m, quantities.xl ];

        this.chart.update();
    }
}
