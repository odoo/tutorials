/** @odoo-module */

console.debug("awesome_dashboard/static/tests/sample_test.js");

QUnit.module("awesome_dashboard", {}, function () {
    QUnit.test("sample test", async function (assert) {
        assert.expect(1);
        assert.ok(true, "This test always passes");
    });
});
