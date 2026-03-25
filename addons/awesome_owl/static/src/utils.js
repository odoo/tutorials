import {useRef, onMounted} from "@odoo/owl"

export function useAutofocus() {
    const ref = useRef('input');
    onMounted(() => {
        ref.el.focus();
    });
    return ref
}