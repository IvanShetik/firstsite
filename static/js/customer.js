$("button[name='btn_delete_customer']").click(function () {
    var data = {cust_id: $(this).data('cust_id')}

    $.ajax({
        type: 'POST',
        url: "/delete_customer",
        data: data,
        dataType: "text",
        success: function (resultData) {
            location.replace('/customers');
        }
    });
});

$("button[name='btn_edit_customer']").click(function () {
    window.location = "edit_customer?cust_id=" + $(this).data('cust_id');
});

$("button[name='btn_new_customer']").click(function() {
    window.location = "new_customer";
});

