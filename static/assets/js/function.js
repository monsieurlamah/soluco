//Adding review
const monthNames = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"];

$('#commentForm').submit(function(e){
    e.preventDefault();

    let dt = new Date();
    let time = dt.getDay() + " " + monthNames[dt.getUTCMonth()] + ", " + dt.getFullYear()

    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr("action"),

        dataType: "json",

        success: function(res){
            console.log("Comment Saved to DB...");

            if (res.bool == true) {
                $("#review-res").html("Avis ajouté avec succès !")
                $(".hide-comment-form").hide()
                $(".add-review").hide()

                let _html = '<div class="single-comment justify-content-between d-flex">'
                    _html += '<div class="user justify-content-between d-flex">'
                    _html += '<div class="thumb text-center">'
                    _html += '<img src="https://cdn-icons-png.flaticon.com/512/6596/6596121.png" alt="'+ res.context.user +'">'
                    _html += '<h6><a href="#">'+ res.context.user +'</a></h6>'
                    _html += '<p class="font-xxs">Depuis ' +time +'</p>'
                    _html += '</div>'
                    _html += ' <div class="desc">'
                    
                    for (let i = 1; i < res.context.rating; i++) {
                        _html += '<i class="fa fa-star text-warning"></i>'
                    }

                    _html += '</div>'
                    _html += '<p>'+ res.context.review +'</p>'
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
$(document).ready(function(){
    $(".filter-checkbox, #price-filter-btn").on("click", function(){
        console.log("Le checkbox a été touché");

        let filter_object = {}

        let min_price = $("#max_price").attr("min")
        let max_price = $("#max_price").val()

        filter_object.min_price = min_price;
        filter_object.max_price = max_price;

        $(".filter-checkbox").each(function() {
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter") //vendor, category

            console.log("La valeur du filtre est:", filter_value);
            console.log("La clé du filtre est:", filter_key);

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter= ' + filter_key + ']:checked')).map(function(element){
                return element.value
            })

        })
        console.log("L'objet filtre est : ", filter_object);
        $.ajax({
            url: '/filter-product', 
            data: filter_object,
            dataType: 'json',
            beforeSend: function() {
                console.log("Essayer de filtrer le produit...");
            },
            success: function(response) {
                console.log(response);
                console.log("Données filtrées avec succès...");
                $("#filtered-product").html(response.data)
            }

        })

    })

    //Filter by price
    $("#max_price").on('blur', function() {
        let min_price = $(this).attr("min")
        let max_price = $(this).attr("max")
        let current_price = $(this).val()

        // console.log("Le prix actuel est ", current_price);
        // console.log("Le prix min est ", min_price);
        // console.log("Le prix max est ", max_price);

        if (current_price < parseInt(min_price) || current_price > parseInt(max_price)) {
            // console.log('Error price occured');

            min_price = Math.round(min_price * 100)/100
            max_price = Math.round(max_price * 100)/100

            // console.log("Le prix min est--- ", min_price);
            // console.log("Le prix max est--- ", max_price);
            alert("Le prix doit être compris entre " + min_price + " GNF " + " et " + max_price + ' GNF')
            $(this).val(min_price)
            $('#range').val(min)


            $(this).focus()
            return false
        }
    })
})