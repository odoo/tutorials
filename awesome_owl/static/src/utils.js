import {useRef,onMounted} from "@odoo/owl";

export function useAutofocus(input) {
    const ref = useRef(input);
    onMounted(() => {
    ref.el.focus();
    });
}
