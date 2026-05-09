$(document).on('click', '.plus-cart-btn', function(){

    var id = $(this).attr("id")
    var quantity = this.parentNode.children[2]

    $.ajax({
        type: 'GET',
        url: '/pluscart',
        data: {
            cart_id: id
        },

        success: function(data){
            console.log(data)

            //  update quantity (top)
            quantity.innerText = data.quantity

            //  update summary
            document.getElementById(`summary${id}`).innerText = data.quantity
            document.getElementById('amount_tt').innerText = data.amount
            document.getElementById('totalamount').innerText = data.total
        },

        error: function(error){
            console.log("ERROR:", error)
        }
    })
})




$(document).on('click', '.minus-cart-btn', function(){

    var id = $(this).attr("id")
    var quantity = this.parentNode.children[2]

    $.ajax({
        type: 'GET',
        url: '/minuscart',
        data: {
            cart_id: id
        },

        success: function(data){
            console.log(data)

            //  update quantity (top)
            quantity.innerText = data.quantity

            //  update summary
            document.getElementById(`summary${id}`).innerText = data.quantity
            document.getElementById('amount_tt').innerText = data.amount
            document.getElementById('totalamount').innerText = data.total
        },

        error: function(error){
            console.log("ERROR:", error)
        }
    })
})



$(document).on('click','.remove-cart', function(){
    var id = $(this).attr("id")
    var to_remove = this.closest('.row')

    $.ajax({
        type: 'GET',
        url: '/remove_cart',
        data: {
            cart_id: id
        },

    success: function(data){
            console.log(data)
            to_remove.remove()
            $(`#summary${id}`).closest('li').remove()
            document.getElementById('amount_tt').innerText = data.amount
            document.getElementById('totalamount').innerText = data.total
        },

    error: function(error){
            console.log("ERROR:", error)
        }
    })

})