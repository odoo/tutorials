import { onMounted, onPatched } from "@odoo/owl";

export function useAutofocus(ref) {
    onMounted(() => {
        if (ref.el) {
            ref.el.focus();
        }
    });
    onPatched(() => {
        if (ref.el) {
            ref.el.focus();
        }
    });
}
