$(document).ready(function(){

getOrgnisationData();
$("#datetimepicker1").datetimepicker({
      format: 'DD/MM/YYYY HH:mm',
    });
$("#add_ordbtn").click(function(){

})

$("#add_Surveybtn").on('click',function(){
    $.ajax({
       type:"GET",
        url: "/newsurvey/getSuvey_list",

      success: function(result) {
        console.log("print result",result)
        alert('ok');
      },
      error: function(result) {
        alert('error');
      }
    });
})

})

function getOrgnisationData(){

   $('#org_table').dataTable({
        "processing": true,
        "serverSide": true,
        "destroy": true,
        "url":"{% url 'getorgdata' %}",
        "searching": true,
        "paging": true,
        "columnDefs": [
            {"targets": 1, "orderable": false},
            {"targets": 2, "orderable": false},
            {"targets": 3, "orderable": false},
            {"targets": 4, "orderable": false},
        ],


        responsive: false,

        "order": [[1, 'asc']],

        "lengthMenu": [[50, 100, 200],[50, 100, 200]],

        "pageLength": 50,
        });

    $('#asset_inspector_table_tools > li > a.tool-action').on('click', function() {
    var action = $(this).attr('data-action');
    $('#org_table').DataTable().button(action).trigger();
    });
}




