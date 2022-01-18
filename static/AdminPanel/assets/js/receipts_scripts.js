"use strict";
$(document).ready(function () {
    //Only needed for the filename of export files.
    //Normally set in the title tag of your page.
    document.title = 'Simple DataTable';
    // DataTable initialisation
    $('#example').DataTable({
        "dom": '<"dt-buttons"Bf><"clear">lirtp',
        "paging": true,
        "autoWidth": true,
        "buttons": [
            'colvis',
            'copyHtml5',
            'csvHtml5',
            'excelHtml5',
            'pdfHtml5',
            'print'
        ]
    });
});
var myArray = [
    {'receipt_id':'11', 'table_id':'13','status':'paid','total_price':'1000','final_price':'900'},
    {'receipt_id':'11', 'table_id':'13','status':'paid','total_price':'1000','final_price':'900'},
    {'receipt_id':'11', 'table_id':'13','status':'paid','total_price':'1000','final_price':'900'},
    {'receipt_id':'11', 'table_id':'13','status':'paid','total_price':'1000','final_price':'900'},
    {'receipt_id':'11', 'table_id':'13','status':'paid','total_price':'1000','final_price':'900'},
    {'receipt_id':'11', 'table_id':'13','status':'paid','total_price':'1000','final_price':'900'},
    {'receipt_id':'11', 'table_id':'13','status':'paid','total_price':'1000','final_price':'900'},
    {'receipt_id':'11', 'table_id':'13','status':'paid','total_price':'1000','final_price':'900'},
    {'receipt_id':'11', 'table_id':'13','status':'paid','total_price':'1000','final_price':'900'},
    {'receipt_id':'11', 'table_id':'13','status':'paid','total_price':'1000','final_price':'900'}
]

function buildOrder(x){
    var table = document.getElementById('order_content')
    table.innerHTML =`<thead>
    <tr style="border: 1px solid black">
      <th style="border: 1px solid black">&nbsp; Food</th>
      <th style="border: 1px solid black">&nbsp; count</th>

    </tr>
    </thead>
    `
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://127.0.0.1:5000/orderbyrid", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
    receipt_id: x
    }));
    console.log(xhr.responseText)
    var lst = JSON.parse(xhr.response);
    for (var i = 0; i < lst.length; i++){

        var row = `<tr style="border: 1px solid black">
                        <td style="border: 1px solid black">&nbsp; ${lst[i]['name']}</td>
                        <td style="border: 1px solid black">&nbsp; ${lst[i]['count']}</td>
                        
                   </tr>`
        table.innerHTML += row
    }
}