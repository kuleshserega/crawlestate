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
    var update_spiders_table = function(){
        $.get(base_scrapyd_url + "listjobs.json?project=crawlestate", function(data){
            var html = '<tr>\
                            <th>ID</th>\
                            <th>Spider name</th>\
                            <th>Start time</th>\
                            <th>End time</th>\
                            <th>Status</th>\
                            <th></th>\
                        </tr>';
            var status = ['running', 'pending', 'finished'];
            for (var i=0; i < status.length; i++) {
                for(var j=0; j < data[status[i]].length; j++) {
                    var btn = '';
                    if (status[i] == 'pending' || status[i] == 'running'){
                        btn = '<a href="' + data[status[i]][j]['id'] + '" class="cancel btn btn-primary">Cancel</a>';
                    }
                    var start_time = '';
                    if (data[status[i]][j]['start_time']){
                        start_time = data[status[i]][j]['start_time'].substring(0,19);
                    }
                    var end_time = '';
                    if (data[status[i]][j]['end_time']){
                        end_time = data[status[i]][j]['end_time'].substring(0,19);
                    }
                    html += '<tr id="' + data[status[i]][j]['id'] + '">\
                            <td>' + data[status[i]][j]['id'] + '</td>\
                            <td>' + data[status[i]][j]['spider'] + '</td>\
                            <td>' + start_time + '</td>\
                            <td>' + end_time + '</td>\
                            <td>' + status[i] + '</td>\
                            <td>' + btn + '</td>\
                        </tr>';
                }
            }
            $('#resultsTable').html(html);
        });
    }

    update_spiders_table();

    var timerId = setInterval(update_spiders_table, 7000);
    
    $(document).on('click', '.cancel', function(e){
        e.preventDefault();
        var job_id = $(this).attr('href');
        var data = {
            'project': 'crawlestate',
            'job': job_id
        }
        $.post(base_scrapyd_url + "cancel.json", data, function(data) {});
    })
    
});