import { Component, useState, onMounted } from "@odoo/owl";
import { Counter } from "./counter";
import { Card } from "./card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card }

    setup() {
        this.taskDone_2 = (param) => {
            this.obj.tasks.find(t => t.task == param ? t.status = true : false);

            console.log({ "tasks": this.obj.tasks });
        };

        this.toggle = (param) => {
            console.log(param);
            //debugger;

            /* -------------------------------------------------------------------------------------
            dont work, ! flip dont work 
            but the asignment works
            */
            //this.obj.tasks.find(t => t.task == param ? t.status.set = !t.status : t.status = t.status)
            //-------------------------------------------------------------------------------------

            /** -------------------------------------------------------------------------------------
             * works because the flip woked inside the considition matching place, 
             * but dont work in the body, 
             * and at the end it returns true because the asignment happed , and executd so
             */
            this.obj.tasks.find(t => t.task == param && (t.status = !t.status));
            //-------------------------------------------------------------------------------------

            /**-------------------------------------------------------------------------------------
             * this already works inside the map,
             * map is mostly used for such types of execution
             */
            //this.obj.tasks.map(t => t.task == param ? t.status = !t.status : t.status = t.status)
            //-------------------------------------------------------------------------------------
            console.log({ "tasks": this.obj.tasks });
        }

        this.newAdd = (param) => {
            this.obj.tasks = [...this.obj.tasks, { "task": param, "status": false }];
        }

        this.handledelete = (param) => {
            this.obj.temp = [];

            const obj = this.obj.tasks

            for (const tasks of obj) {

                if (tasks.task == param) {
                    this.obj.temp = [...this.obj.temp]
                }
                else {
                    this.obj.temp = [...this.obj.temp, { "task": tasks.task, "status": tasks.status }];
                }
            }
            this.obj.tasks = [];

            this.obj.tasks = [...this.obj.temp];
            console.log({ "temp": this.obj.temp });
            console.log({ "tasks": this.obj.tasks });
            this.obj.temp = [{}];
        }

        this.obj = useState({ tasks: [{ type: Object, write: true }], temp: [{ type: Object }] });
        this.obj.tasks = [
            { 'task': "add_color", "status": true },
            { 'task': "code0", "status": true },
            { 'task': "code1", "status": true },
            { 'task': "code2", "status": false },
            { 'task': "code3", "status": false },
            { 'task': "code4", "status": false },
            { 'task': "code5", "status": false }
        ]

        console.log(this);
    }


}
