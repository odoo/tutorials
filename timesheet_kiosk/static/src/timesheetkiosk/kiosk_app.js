/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import {useService} from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { StartScreen } from "./start_screen/start_screen";
import { TaskScreen } from "./task_screen/task_screen";
import { TaskScreen2 } from "./task_screen2/task_screen2";


export class KioskApp extends Component {
    static template = "timesheet_kiosk.KioskApp";
    static components = { Layout, StartScreen, TaskScreen , TaskScreen2 };

    setup() {
        this.state = useState({
            screen: "start",
            employee: null,
            tasks: [],
            projects: [],
            timer: false,
            timertask: null,
            timmerproject: null,
            timerlineid: null,
        });
        this.orm = useService("orm");
    }

    onEmployeeFound(employee, tasks, projects, timer, timertask, timmerproject, timerlineid) {
        this.state.employee = employee;
        this.state.tasks = tasks;
        this.state.projects = projects;
        this.state.timer = timer;
        this.state.timertask = timertask;
        this.state.timmerproject = timmerproject;
        this.state.timerlineid = timerlineid;

        if (timer == true) {
            this.state.screen = "task_running";
        } else {
            this.state.screen = "task";
        }
    }

    goToStart() {
        this.state.employee = null;
        this.state.tasks = [];
        this.state.projects = [];
        this.state.timmerproject = null;
        this.state.timertask = null;
        this.state.timerlineid = null;
        this.state.screen = "start";
    }

    async startTimer(taskId) {
        await this.orm.call(
            "project.task",
            "action_timer_start",
            [[taskId]]
        );
        this.state.screen = "start";
    }

    async stopTimer(timerLineId) {
        await rpc('/timesheet_kiosk/stop_timer', {
            timer_line_id: timerLineId,
            employee_id: this.state.employee.id,
        });
        this.state.screen = "start";
    }
}

registry.category("actions").add("timesheet_kiosk", KioskApp);
