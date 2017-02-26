var p1=[0,1,2,3,4];
var p2=[0,1];
var p3=[0,1,5,7];
var p4=[0,1,12,44];
var p5=[0,1,2,3,4,5,6,7,8,9,10,12,44,11];

function isemptyfloor() {
    for(var i =0 ;i<5;i++)
        if(floor_now[i] == 1)
            return 0;
        else return 1;
}

function culprit(cust,floor) {
    if(cust == 1)
    {
        if($.inArray(floor,p1) > -1)
        {return 0;
        }
    }
    else if(cust ==2)
    {
        if($.inArray(floor,p2) > -1)
        {
            return 0;
        }

    }else if(cust ==3){

        if($.inArray(floor,p3) > -1)
        {
            return 0;
        }

    }
    else if(cust ==4)
    {
        if($.inArray(floor,p4) > -1)
        {
            return 0;
        }

    }else{

        if($.inArray(floor,p5) > -1)
        {
            return 0;
        }

    }
    return 1;
}

$(document).ready(function(){
    console.log('Laura');
    $("#authentication *").prop('disabled',true);
    $('#authentication').prop('disabled',true);
    $("#control_panel *").prop('disabled',true);
    $("#control_panel").prop('disabled',true);
    $("#elevatorstatus *").prop('disabled',true);
    $("#elevatorstatus").prop('disabled',true);
    $('.person_press').prop('disabled',true);
    var cur_floor = 1;

    var people_now = [];
    var floor_now = [];

    var peoplecount,pressurecount,authcount;

    $('form').submit(function (event) {
        peoplecount = $('#people_count').val();
        pressurecount = $('#pressure_count').val();
        authcount = $('#person_data').val();

        $('#formpeople').prop('disabled',true)
        $('#formpeople *').prop('disabled',true);

        $("#authentication *").prop('disabled',false);
        $('#authentication').prop('disabled',false);
        $("#control_panel *").prop('disabled',false);
        $("#control_panel").prop('disabled',false);
        $("#elevatorstatus *").prop('disabled',false);
        $("#elevatorstatus").prop('disabled',false);
        $('.person_press').prop('disabled',false);

        //Assert All variables here

        if(peoplecount == authcount)
        {
            if(authcount == pressurecount/2)
            {
                //Do Nothing
            }else{
                window.alert('Incorrect Intial Info');
                window.location.href('');
            }
        }
        else{
            window.alert('Incorrect Initial Info');
            window.location.href('');
        }

        // End Assert
        $('#refresh').prop('disabled',false);
        return event.preventDefault();

    });

    $('.person_press').click(function () {

        console.log('Clicl');
        var temp_id = $(this).attr('id');
        temp_id = temp_id.substr(1);
        temp_id = parseInt(temp_id);

        if(culprit(temp_id,cur_floor) == 1)
        {
            window.alert('Unauthorized Traverse by person at floor '+cur_floor);
        }

        if(people_now[temp_id]!=1)
        {
            people_now[temp_id] = 1;
            console.log('fuck');
            $(this).text(($.trim($(this).text().substring(0,7)))+'-');
            $('#authentication').append('<div id="ptext'+ temp_id +'"><h4><b>People '+ temp_id +'</b></h4></div>');
        }
        else{
            $(this).text(($.trim($(this).text().substring(0,7)))+'+');
            people_now[temp_id] = 0;
            $('#ptext'+temp_id).remove();
        }
    });
    
    $('.floor_btn').click(function () {
        if(floor_now[$(this).attr('id').substr(1)] != 1)
        {   $(this).addClass('btn-warning');
            floor_now[$(this).attr('id').substr(1)] = 1;
        }
        else
        {   $(this).removeClass('btn-warning');
            floor_now[$(this).attr('id').substr(1)] = 0;}
    });

    $('#gobtn').click(function () {
       var next_floor = -1;

       for(var i =1 ;i<=5;i++)
       {
           if(floor_now[i] == 1)
           {
               cur_floor = i;
               next_floor = i;
               floor_now[i] = 0;
               $('#f'+i).removeClass('btn-warning');
               console.log(floor_now[i]);
               break;
           }

       }
       $('#elevator_status').val('Running');

       $('#fordelay').slideUp(0).delay(3000).slideDown(0);

       $('#elevator_status').val('Halt');

       $('#floor_input').val(cur_floor);
       console.log(cur_floor);

    });


});
