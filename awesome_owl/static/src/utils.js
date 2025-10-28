import { useRef, onMounted } from "@odoo/owl";


const useAutofocus = (refName) => {
    const ref = useRef(refName)
    onMounted(() => ref.el.focus())
}


export {
    useAutofocus
}