$(function () {
//一起用runoob js: https://www.runoob.com/jqueryui/example-accordion.html
//sortable 排序
    $("#sortable").sortable();
    $("#sortable").disableSelection();

//    以上好似相似 類似參考: https://github.com/mdbootstrap/mdb-docs-and-content/blob/master/en/jquery/web/docs/plugins/sortable/o.html
//    MDB : https://mdbootstrap.com/plugins/jquery/sortable/

});

//-------------------------------------------------product.html--------------------------------------------------------------
// Horizontal scrolling table with Fixed first column
$('table').on('scroll', function () {
    $("#" + this.id + " > *").width($(this).width() + $(this).scrollLeft());
});
//-------------------------------------------------product.html--------------------------------------------------------------
var tag = 1;
$(function () {
    $("#add").click(function () {
        $('#table1 tbody').before('<tr><td>No.' + tag + '</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td class="text-center">\n' +
            '                                            <!-- Call to action buttons -->\n' +
            '                                            <ul class="list-inline m-0">\n' +
            '                                                <li class="list-inline-item">\n' +
            '                                                    <button id="add" class="btn btn-primary btn-sm rounded-0" type="button"\n' +
            '                                                            data-toggle="tooltip" data-placement="top" title="Add"><i\n' +
            '                                                            class="fa fa-plus-square" aria-hidden="true"></i></button>\n' +
            '                                                </li>\n' +
            '                                                <li class="list-inline-item">\n' +
            '                                                    <button class="btn btn-success btn-sm rounded-0" type="button"\n' +
            '                                                            data-toggle="tooltip" data-placement="top" title="Edit"><i\n' +
            '                                                            class="fa fa-edit"></i></button>\n' +
            '                                                </li>\n' +
            '                                                <li class="list-inline-item">\n' +
            '                                                    <button id="del" class="btn btn-danger btn-sm rounded-0" type="button"\n' +
            '                                                            data-toggle="tooltip" data-placement="top" title="Delete"><i\n' +
            '                                                            class="fa fa-trash"></i></button>\n' +
            '                                                </li>\n' +
            '                                            </ul>\n' +
            '                                        </td></tr>');
        tag++;
    });
    $("#del").click(function () {
        $("#table1 tbody tr:last").remove();
    });
})
