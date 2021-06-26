$("button[name='btn_delete_vendor']").click(function () {
    var data = {vend_id: $(this).data('vend_id')}

    $.ajax({
        type: 'POST',
        url: "/delete_vendor",
        data: data,
        dataType: "text",
        success: function (resultData) {
            location.replace('/vendors');
        }
    });
});

$("button[name='btn_edit_vendor']").click(function () {
    window.location = "edit_vendor?vend_id=" + $(this).data('vend_id');
});

$("button[name='btn_new_vendor']").click(function() {
    window.location = "new_vendor";
});

