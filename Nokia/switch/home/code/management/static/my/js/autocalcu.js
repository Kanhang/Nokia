/**
 * Created by tisong on 2017/11/20.
 */

(function($) {
    'use strict';
    $(function() {
        $(".field-Status").each(function(){
             var status = $(this).find("select").val();
             if(status == "Done"){
                 $(this).next().find("input").val("100%");
             }
             var progress = $(this).next().find("input").val()

        });

        $(".field-Progress").each(function () {
            var progress = $(this).find("input").val();
            progress = progress.replace(/[^0-9]/g,"")/100;
            var status = $(this).siblings(".field-Status").find("select").val();
            var end = $(this).siblings(".field-End_time").find("input").val();
            var start = $(this).siblings(".field-Start_time").find("input").val();
            var start_time = new Date(start);
            var end_time = new Date(end);
            var now = new Date();
            var temp= ((now.getTime() - start_time.getTime()) / 86400000)/((end_time.getTime() - start_time.getTime()) / 86400000);
            if(status == "Ongoing"){
                if(temp>=0 && temp<=1){
                    if(temp>progress){
                        $(this).siblings(".field-Condition").find("select").val("Delay");
                    }
                    else{
                        $(this).siblings(".field-Condition").find("select").val("Ontime");
                    }
                }
                else{
                    if(progress==1){
                        $(this).siblings(".field-Condition").find("select").val("Ontime");
                    }
                }
            }
            else{
                $(this).siblings(".field-Condition").find("select").val(null);
            }
            console.log(status);
            console.log($(this).siblings(".field-Condition").find("select").val());
        })


    });
})(django.jQuery);

