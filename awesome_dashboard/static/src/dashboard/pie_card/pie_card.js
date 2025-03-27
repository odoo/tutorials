import { Component, onMounted, useState, onWillRender, markup, onWillPatch, onWillUpdateProps } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { Card } from "../card/card";


export class PieCard extends Component {
    static template = 'pie_card.pie_card';
    static components = { Card };
    static props = {
        title: {type: 'String', optional: 'true',},
        data: {type: 'Object', optional: 'true',},
        size: {type: 'Number', optional: 'true',},
        id: {type: 'String', optional: 'true',},
        stringProps: {type: 'String', optional: 'true',},
        registerUpdate: {type: 'Function', optional: 'true',},
    };

    setup() {
        if (this.props.stringProps) {
            this.stringProps = JSON.parse(this.props.stringProps);

            this.id = this.stringProps.id ? this.stringProps.id : 'piechart'

            this.data = this.stringProps.data ? this.stringProps.data : {'no data.': 1};

            this.size = this.stringProps.size;

            this.title = this.stringProps.title;
        } else {
            this.id = this.props.id ? this.props.id : 'piechart'

            this.data = this.props.data ? this.props.data : {'no data.': 1};

            this.size = this.props.size;

            this.title = this.props.title;
        }
        

        if (this.props.registerUpdate) {
            if ((this.props.stringProps != null && this.props.stringProps != undefined) && this.stringProps.source) {
                this.props.registerUpdate(() => {
                    if (this.chart) {
                        this.chart.destroy();
                    }
                });
            }
        }


        this.state = useState({data: null});

        this.chart = null;


        this.canvas = markup(`
            <canvas id="${this.id}">
            </canvas>
        `);
        this.render = async () => {
            
            this.context = document.getElementById(this.id);
            if (this.context == null || this.context == undefined) {
                return;
            }

            try {
                this.chart.clear();
            } catch (exception) {
            }

            const chartJS = await loadJS("/web/static/lib/Chart/Chart.js");

            const config = {
                type: 'pie',
                data: {
                    labels: Object.keys(this.data),
                    datasets: [
                        {
                            label: 'ds1',
                            data: Object.values(this.data),
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
            /*
            // epilepsy mode
            this.context.onmousemove = () => {
                const hex = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
                const genHex = () => `${hex[Math.floor(Math.random() * 16)]}${hex[Math.floor(Math.random() * 16)]}`
                const genColor = () => `#${genHex()}${genHex()}${genHex()}`
                this.context.style.backgroundColor = genColor();
            }
            */
        });


    }
}
