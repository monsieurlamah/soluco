//Adding review
const monthNames = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"];

$('#commentForm').submit(function (e) {
    e.preventDefault();

    let dt = new Date();
    let time = dt.getDay() + " " + monthNames[dt.getUTCMonth()] + ", " + dt.getFullYear()

    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr("action"),

        dataType: "json",

        success: function (res) {
            console.log("Comment Saved to DB...");

            if (res.bool == true) {
                $("#review-res").html("Avis ajouté avec succès !")
                $(".hide-comment-form").hide()
                $(".add-review").hide()

                let _html = '<div class="single-comment justify-content-between d-flex">'
                _html += '<div class="user justify-content-between d-flex">'
                _html += '<div class="thumb text-center">'
                _html += '<img src="https://cdn-icons-png.flaticon.com/512/6596/6596121.png" alt="' + res.context.user + '">'
                _html += '<h6><a href="#">' + res.context.user + '</a></h6>'
                _html += '<p class="font-xxs">Depuis ' + time + '</p>'
                _html += '</div>'
                _html += ' <div class="desc">'

                for (let i = 1; i < res.context.rating; i++) {
                    _html += '<i class="fa fa-star text-warning"></i>'
                }

                _html += '</div>'
                _html += '<p>' + res.context.review + '</p>'
                _html += '<div class="d-flex justify-content-between">'
                _html += '<div class="d-flex align-items-center">'
                _html += '<p class="font-xs mr-30"></p>'
                _html += '</div>'
                _html += '</div>'
                _html += '</div>'
                _html += '</div>'
                _html += '</div>'

                $(".comment-list").prepend(_html)
            }

        }
    })
})


// Filter by category and vendor no-refresh 
$(document).ready(function () {
    $(".filter-checkbox, #price-filter-btn").on("click", function () {
        console.log("Le checkbox a été touché");

        let filter_object = {}

        let min_price = $("#max_price").attr("min")
        let max_price = $("#max_price").val()

        filter_object.min_price = min_price;
        filter_object.max_price = max_price;

        $(".filter-checkbox").each(function () {
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter") //vendor, category

            console.log("La valeur du filtre est:", filter_value);
            console.log("La clé du filtre est:", filter_key);

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter= ' + filter_key + ']:checked')).map(function (element) {
                return element.value
            })

        })
        console.log("L'objet filtre est : ", filter_object);
        $.ajax({
            url: '/filter-product',
            data: filter_object,
            dataType: 'json',
            beforeSend: function () {
                console.log("Essayer de filtrer le produit...");
            },
            success: function (response) {
                console.log(response);
                console.log("Données filtrées avec succès...");
                $("#filtered-product").html(response.data)
            }

        })

    })

    //Filter by price
    $("#max_price").on('blur', function () {
        let min_price = $(this).attr("min")
        let max_price = $(this).attr("max")
        let current_price = $(this).val()

        // console.log("Le prix actuel est ", current_price);
        // console.log("Le prix min est ", min_price);
        // console.log("Le prix max est ", max_price);

        if (current_price < parseInt(min_price) || current_price > parseInt(max_price)) {
            // console.log('Error price occured');

            min_price = Math.round(min_price * 100) / 100
            max_price = Math.round(max_price * 100) / 100

            // console.log("Le prix min est--- ", min_price);
            // console.log("Le prix max est--- ", max_price);
            alert("Le prix doit être compris entre " + min_price + " GNF " + " et " + max_price + ' GNF')
            $(this).val(min_price)
            $('#range').val(min)


            $(this).focus()
            return false
        }
    })
    // Add to cart functional
    $(".add-to-cart-btn").on("click", function () {

        let this_val = $(this)
        let index = this_val.attr("data-index")

        let quantity = $(".product-quantity-" + index).val()
        let product_title = $(".product-title-" + index).val()

        let product_id = $(".product-id-" + index).val()
        let product_price = $(".current-product-price-" + index).text()

        let product_pid = $(".product-pid-" + index).val()
        let product_image = $(".product-image-" + index).val()


        console.log("Quantité: ", quantity);
        console.log("Le titre du produit: ", product_title);
        console.log("Le prix du produit: ", product_price);
        console.log("ID: ", product_id);
        console.log("PID: ", product_pid);
        console.log("Image: ", product_image);
        console.log("Index: ", index);
        console.log("L'element actuel", this_val);

        $.ajax({
            url: '/add-to-cart',
            data: {
                'id': product_id,
                'pid': product_pid,
                'image': product_image,
                'qty': quantity,
                'title': product_title,
                'price': product_price,
            },
            dataType: "json",
            beforeSend: function () {
                console.log("Ajouter un produit au panier...");
            },
            success: function (response) {
                this_val.html("✔")
                console.log("Produit ajouté au panier !");

                $(".cart-items-count").text(response.totalcartitems)
            }
        })
    })

    //Delete product from cart. 
    $(".delete-product").on("click", function () {
        let product_id = $(this).attr("data-product")
        let this_val = $(this)

        console.log("ID du produit: ", product_id);

        $.ajax({
            url: '/delete-from-cart',
            data: {
                "id": product_id,
            },
            dataType: "json",
            beforeSend: function () {
                this_val.hide()
            },
            success: function (response) {
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
            }
        })

    })

    //update product from cart. 
    $(".update-product").on("click", function () {
        let product_id = $(this).attr("data-product")
        let this_val = $(this)
        let product_quantity = $('.product-qty-' + product_id).val()

        console.log("ID du produit: ", product_id);
        console.log("Product QTY: ", product_quantity);

        $.ajax({
            url: '/update-cart',
            data: {
                "id": product_id,
                "qty": product_quantity,
            },
            dataType: "json",
            beforeSend: function () {
                this_val.hide()
            },
            success: function (response) {
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
            }
        })

    })

    // Making Defaut Address
    $(document).on("click", ".make-default-address", function () {
        let id = $(this).attr("data-address-id")
        let this_val = $(this)

        console.log("ID est:", id);
        console.log("Element est:", this_val);

        $.ajax({
            url: "/make-default-address",
            data: {
                "id": id,
            },
            dataType: "json",
            success: function (response) {
                console.log("Adresse par défaut...");
                if (response.boolean == true) {
                    $(".check").hide()
                    $(".action_btn").show()

                    $(".check" + id).show()
                    $(".button" + id).hide()
                }
            }
        })
    })

    //adding to wishlist
    $(document).on("click", ".add-to-wishlist", function () {
        let product_id = $(this).attr("data-product-item")
        let this_val = $(this)

        console.log("ID du produit est: ", product_id);

        $.ajax({
            url: "/add-to-wishlist",
            data: {
                "id": product_id
            },
            dataType: 'json',
            beforeSend: function () {
                console.log("Adding to wishlist...");
            },
            success: function (response) {
                this_val.html("✔")
                if (response.bool === true) {
                    console.log("Added to wishlist...");
                }
            }
        })
    })

    //remove from wishlist
    $(document).on("click", ".delete-wishlist-product", function () {
        let wishlist_id = $(this).attr("data-wishlist-product")
        let this_val = $(this)

        console.log("Wishlist ID est: ", wishlist_id);

        $.ajax({
            url: "/remove-from-wishlist",
            data: {
                "id": wishlist_id,
            },
            dataType: "json",
            beforeSend: function () {
                console.log("Deleting product from wishlist...");
            },
            success: function (response) {
                $("#wishlist-list").html(response.data)
            }
        })
    })

    $(document).on('submit', "#contact-form-ajax", function (e) {
        e.preventDefault()
        console.log("submited...");

        let full_name = $("#full_name").val();
        let email = $("#email").val();
        let phone = $("#phone").val();
        let subject = $("#subject").val();
        let message = $("#message").val();

        console.log("Nom complet: ", full_name);
        console.log("Email: ", email);
        console.log("Téléphone: ", phone);
        console.log("Message: ", message);

        $.ajax({
            url: '/ajax-contact-form',
            data: {
                'full_name': full_name,
                'email': email,
                'phone': phone,
                'subject': subject,
                'message': message,
            },
            dataType: 'json',
            beforeSend: function () {
                console.log("Sending Data to Server...");
            },
            success: function (res) {
                console.log("Sent Data to server !");
                $("#contact_us_p").hide()
                $("#contact-form-ajax").hide()
                $("#message-response").html("Message sent successfully !")
            }
        })

    })

})







// Add to cart functional
// $("#add-to-cart-btn").on("click", function(){
//     let quantity = $("#product-quantity").val()
//     let product_title = $(".product-title").val()
//     let product_id = $(".product-id").val()
//     let product_price = $("#current-product-price").text()
//     let this_val = $(this)


//     console.log("Quantité: ", quantity);
//     console.log("Le titre du produit: ", product_title);
//     console.log("Le prix du produit: ", product_price);
//     console.log("ID: ", product_id);
//     console.log("L'element actuel", this_val);

//     $.ajax({
//         url: '/add-to-cart',
//         data: {
//             'id':product_id,
//             'qty':quantity,
//             'title':product_title,
//             'price':product_price,
//         },
//         dataType: "json",
//         beforeSend: function () {
//             console.log("Ajouter un produit au panier...");
//         },
//         success:function (response) {
//             this_val.html("Article ajouté au panier")
//             console.log("Produit ajouté au panier !");

//             $(".cart-items-count").text(response.totalcartitems)
//         }
//     })
// })