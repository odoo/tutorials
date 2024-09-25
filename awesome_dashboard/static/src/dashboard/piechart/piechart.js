/** @odoo-module **/

import { Component, useState, onWillStart, useRef, onMounted, onWillUnmount, useEffect} from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { getColor } from "@web/core/colors/colors";


export class PieChart extends Component {

    static template = "awesome_dashboard.piechart";

    static props = {
        data: {type: Object}
    }

    setup(){

        this.canvasRef = useRef("canvas");
        onWillStart(async () => loadJS(["/web/static/lib/Chart/Chart.js"]));
        useEffect(() => {this.renderChart()})

    }


    renderChart(){
        if(this.chart){
            this.chart.destroy()
        }
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        const color = labels.map((_, index) => getColor(index));
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.label,
                        data: data,
                        backgroundColor: color
                    }
                ]
            }
        });
    }
}