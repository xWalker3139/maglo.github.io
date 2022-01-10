$(document).ready(function(){
    $("#select").change(function(){
    $(this).find("option:selected").each(function(){
        var optionValue = $(this).attr("id");
        if(optionValue){
            $(".box").not("." + optionValue).hide();
            $("." + optionValue).show();
        } else{
            $(".box").hide();
        }
    });
}).change();
})
$(document).ready(function(){
    $("#selectare").change(function(){
    $(this).find("option:selected").each(function(){
        var optionValue = $(this).attr("id");
        if(optionValue){
            $(".newbox").not("." + optionValue).hide();
            $("." + optionValue).show();
        } else{
            $(".newbox").hide();
        }
    });
}).change();
})
$(document).ready(function(){
    $("#mybox").change(function(){
    $(this).find("option:selected").each(function(){
        var optionValue = $(this).attr("id");
        if(optionValue){
            $(".mybox").not("." + optionValue).hide();
            $("." + optionValue).show();
        } else{
            $(".mybox").hide();
        }
    });
}).change();
})
$(document).ready(function(){
    $("#mybox2").change(function(){
    $(this).find("option:selected").each(function(){
        var optionValue = $(this).attr("id");
        if(optionValue){
            $(".mybox2").not("." + optionValue).hide();
            $("." + optionValue).show();
        } else{
            $(".mybox2").hide();
        }
    });
}).change();
})
$(document).ready(function(){
    $("#mybox3").change(function(){
    $(this).find("option:selected").each(function(){
        var optionValue = $(this).attr("id");
        if(optionValue){
            $(".mybox3").not("." + optionValue).hide();
            $("." + optionValue).show();
        } else{
            $(".mybox3").hide();
        }
    });
}).change();
})