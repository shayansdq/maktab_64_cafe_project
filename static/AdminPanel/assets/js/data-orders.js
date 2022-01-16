(function ($) {
    'use strict';
    var dataSet = [
        ["56454", "<img src='../../assets/img/costic/cereals.jpg' style='width:50px; height:30px;color: black'>cake", "5407", "Out Of Stock", "$16", "<a href='#'><i class='fas fa-pencil-alt text-secondary'></i></a> <a href='a'><i class='far fa-trash-alt ms-text-danger'></i></a>"],
        ["14451", "<img src='../../assets/img/costic/french-fries.jpg' style='width:50px; height:30px; color: black'>pizza", "5384", "Out Of Stock", "$85", "<a href='#'><i class='fas fa-pencil-alt text-secondary'></i></a> <a href='a'><i class='far fa-trash-alt ms-text-danger'></i></a>"]
    ];
    var tableTwo = $('#data-table-2').DataTable({
        data: dataSet,
        columns: [
            {title: "Product ID"},
            {title: "Product Name"},
            {title: "Quantity"},
            {title: "Status"},
            {title: "Price"}
        ],
    });
})(jQuery);
