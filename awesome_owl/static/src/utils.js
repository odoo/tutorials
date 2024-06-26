/** @odoo-module **/

import { useRef, onMounted} from "@odoo/owl";

export function useAutofocus(ref_string) {
    const inputTodoRef = useRef(ref_string);
    onMounted(() => {
        inputTodoRef.el.focus();
    });
}
