import {useRef, onMounted} from "@odoo/owl"

export function useAutofocus(reference) {
    const myRef = useRef(reference)
    onMounted(() => {
        myRef.el.focus()
    });
}