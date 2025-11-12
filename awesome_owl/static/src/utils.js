import { onMounted } from "@odoo/owl";


export class Utils {
    static useAutofocus(ref) {
        onMounted(() => {
            if (ref.el) {
                ref.el.focus();
            }
        });
    }
}
