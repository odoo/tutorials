function selectAuctionStage(stage) {
    const model = 'estate.property';
    const recordId = parseInt($("form.o_form_editable").data('id')); 

    if (!recordId) {
        alert("No record found to update.");
        return;
    }

    ajax.jsonRpc('/web/dataset/call_kw', 'call', {
        model: model,
        method: 'action_set_auction_stage',
        args: [[recordId], stage],
        kwargs: {},
    }).then(() => {
        location.reload();
    }).catch(error => console.error("Error updating stage:", error));
}
