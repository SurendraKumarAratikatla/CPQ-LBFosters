
cpq.events.sub("API:cart:updated",function(data){
    var flag = false
    $('tbody#itemsTable tr').each(function(index){
        var column = $(this).children('td');
        $(column).each(function(index1){
            var column_data_title = $(this).attr('data-title');
                if (column_data_title == 'Plant'){
                    $(this);
                }
                else if (column_data_title == 'Hnd.Cost.Unit'){
                    $(this).find('a').css('cssText','border-bottom: 0;color: #303133;pointer-events: none;');
                }
        })
    })
})