import { onMounted } from "@odoo/owl";

export default useAutofocus = (ref) => {
  onMounted(() => {
    ref.el.focus();
  });
};
