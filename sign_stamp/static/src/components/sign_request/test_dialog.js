import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class TestDialog extends Component {
    static template = "sign_stamp.test_dialog";
    static components = { Dialog };
}
