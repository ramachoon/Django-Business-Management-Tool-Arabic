// get csrf token from cookies
const csrf_token = KTCookie.getCookie('csrftoken')

// modals
let kalaDetailModal = $('#kalaDetailModal')

// actions
let kalaDetailAction = ''

// get kala details modal inputs
let inputKalaDetailId = $('#inputKalaDetailId')
let inputKalaDetailName = $('#inputKalaDetailName')
let inputKalaDetailQuantity = $('#inputKalaDetailQuantity')
let inputKalaDetailPrice = $('#inputKalaDetailPrice')
let inputKalaDetailTotal = $('#inputKalaDetailTotal')

// set data for kala details modal inputs
function setKalaDetailForm(id, name, quantity, price, total) {
    inputKalaDetailId.val(id)
    inputKalaDetailName.val(name)
    inputKalaDetailQuantity.val(quantity)
    inputKalaDetailPrice.val(price)
    inputKalaDetailTotal.val(total)
}

// reset kala details modal input
function resetKalaDetailForm() {
    inputKalaDetailId.val("")
    inputKalaDetailName.val("")
    inputKalaDetailQuantity.val("")
    inputKalaDetailPrice.val("")
    inputKalaDetailTotal.val("")
}

// kala details modal close btn
$('#close-kala-detail-btn').click(function () {
    resetKalaDetailForm()
})

// submit kala detail form function
function submitKalaDetailForm() {
    /*\
    * if kalaDetailAction is equal to create, the request be send to /manager/storeroom/kala-details/create
    * else if kalaDetailAction is equal to update, the request be send to /manager/storeroom/kala-details/update.
    * */

    if (kalaDetailAction === 'create') {
        $.ajax({
            'url': '/manager/storeroom/kala-details/create',
            'method': 'POST',
            data: {
                'csrfmiddlewaretoken': csrf_token,
                'kala_id': kala_id,
                'kala_detail_name': inputKalaDetailName.val(),
                'kala_detail_quantity': inputKalaDetailQuantity.val(),
                'kala_detail_price': inputKalaDetailPrice.val(),
                'kala_detail_total': inputKalaDetailTotal.val()
            }
        }).done(function (data) {
            if (data.status === 'success') {
                $('#kala-detail-table').html(data.template)
            }
        })
    } else if (kalaDetailAction === 'update') {
        $.ajax({
            url: '/manager/storeroom/kala-details/update',
            method: 'POST',
            data: {
                'csrfmiddlewaretoken': csrf_token,
                'kala_id': kala_id,
                'kala_detail_id': inputKalaDetailId.val(),
                'kala_detail_name': inputKalaDetailName.val(),
                'kala_detail_quantity': inputKalaDetailQuantity.val(),
                'kala_detail_price': inputKalaDetailPrice.val(),
                'kala_detail_total': inputKalaDetailTotal.val()
            }
        }).done(function (data) {
            $('#kala-detail-table').html(data.template)
        })
    }

    resetKalaDetailForm()
    kalaDetailAction = ''

    kalaDetailModal.modal('hide')
}

function editKalaDetail(self) {
    /*
    * this function is called when a KalaDetail needs to be update.
    * */

    kalaDetailAction = 'update'

    let kalaDetailId = $(self).parent().parent().attr('data-kala-detail-id')
    let kalaDetailName = $(self).parent().parent().children('.kala-detail-name').text()
    let kalaDetailQuantity = $(self).parent().parent().children('.kala-detail-quantity').text()
    let kalaDetailPrice = $(self).parent().parent().children('.kala-detail-price').text()
    let kalaDetailTotal = $(self).parent().parent().children('.kala-detail-total').text()

    setKalaDetailForm(kalaDetailId, kalaDetailName, kalaDetailQuantity, kalaDetailPrice, kalaDetailTotal)

    kalaDetailModal.modal('show')
}

$('#createKalaDetail').click(function () {
    kalaDetailAction = 'create'
    kalaDetailModal.modal('show')
})

$('#send-kala-detail-btn').click(function () {
    submitKalaDetailForm('create')
})

function deleteKalaDetail(self) {
    /*
    * this function is called when a kalaDetail needs to be delete.
    * */

    let kalaDetailId = $(self).attr('id')
    $.ajax({
        'url': '/manager/storeroom/kala-details/delete',
        'method': "POST",
        data: {
            'csrfmiddlewaretoken': csrf_token,
            'kala_id': kala_id,
            'kala_detail_id': kalaDetailId
        }
    }).done(function (data) {
        $("#kala-detail-table").html(data.template)
    })
}