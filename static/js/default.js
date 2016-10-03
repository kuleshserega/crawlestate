// $(document).ready(function(){
//     $('.messages').find('.alert').each(function(){
//         var el = $(this);
//         setTimeout(function(){
//             el.fadeOut(500, function(){
//                el.remove();
//             });
//         }, 4000);
//     });
// });
var base_scrapyd_url = 'http://localhost:6800/';

$(document).ready(function(){
    $.get(base_scrapyd_url + "listjobs.json?project=crawlestate", function(data){
        console.log("Data: " + data);
        var html = '';
        var status = ['running', 'finished', 'pending'];
        for (var i=0; i < status.length; i++) {
            for(var j=0; j < data[status[i]].length; j++) {
                var btn = '';
                if (status[i] == 'pending' || status[i] == 'running'){
                    btn = '<a href="' + data[status[i]][j]['id'] + '" class="cancel btn btn-primary">Cancel</a>';
                }
                html += '<tr id="' + data[status[i]][j]['id'] + '">\
                        <td>' + data[status[i]][j]['id'] + '</td>\
                        <td>' + data[status[i]][j]['spider'] + '</td>\
                        <td>' + data[status[i]][j]['start_time'] + '</td>\
                        <td>' + data[status[i]][j]['end_time'] + '</td>\
                        <td>' + status[i] + '</td>\
                        <td>' + btn + '</td>\
                    </tr>';
            }
        }
        $('table tr').after(html);
    });
    
    $(document).on('click', '.cancel', function(e){
        console.log('TRY');
        e.preventDefault();
        var job_id = $(this).attr('href');
        var data = {
            'project': 'crawlestate',
            'job': job_id
        }
        $.post(base_scrapyd_url + "cancel.json", data, function(data) {
          console.log( data );
        });
    })
    
});