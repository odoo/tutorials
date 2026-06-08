
import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

export class StartScreen extends Component {
    static template = "timesheet_kiosk.StartScreen";

    static props = {
        onEmployeeFound: Function,
    };

    setup() {
        this.state = useState({
            barcode: "",
            error: "",
        });

        this.inputRef = useRef("input");
        onMounted(() => {
            this.inputRef.el.focus();
        });
    }

    async onSearch() {
        if (!this.state.barcode) return;

        const result = await rpc('/timesheet_kiosk/get_employee_data', {
            barcode: this.state.barcode,
        });

        if (result.error) {
            this.state.error = result.error;
        } else {
            this.state.error = "";
            this.props.onEmployeeFound(result.employee, result.tasks, result.projects, result.timer, result.timertask, result.timmerproject, result.timerlineid);
        }
    }

    onKeyUp(ev) {
        if (ev.keyCode === 13) this.onSearch();
    }
}
