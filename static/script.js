$(document).ready(function(){

    // Book search  
    $("#books").keyup(function(){
        var data = $("#search_form").serialize()
        $.ajax({
            method: "GET",
            url: "/search",
            data: data
        })
        .done(function(res){
            $("#search_result").html(res)
        })         
    })

    // User posted review
    $("#review_submit").submit(function(e){
        e.preventDefault()
        var data = $("#review_form").serialize()
        var book_id = $("#bookId").val()
        $.ajax({
            method: "POST",
            url: "/reviews/"+book_id,
            data: data
        })
        .done(function(res){
            console.log(res)
            return res
        })
    })

    
    // Book reviews
    $(window).ready(function(){
        var book_id = $("#bookId").val()
        $.ajax({
            method: "GET",           
            url: "/reviews/"+book_id,
        })
        .done(function(response){
            $("#all_reviews").html(response)
        })
    })

})