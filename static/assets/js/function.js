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


// Filter no-refresh
$(document).ready(function(){
    $(".filter-checkbox").on("click", function(){
        console.log("Le checkbox a été touché");

        let filter_object = {}

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
})