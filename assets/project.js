
$(document).ready(function () {
    $.getJSON('http://localhost:8000/fetch_all_category_json',function (data) {
      var records=data.data
      records.map((item)=>{
          $('#categoryid').append($("<option>").text(item.categoryname).val(item.categoryid))

      })
        $('select').formSelect();
    })


 $('#categoryid').change(function (){
        $('#subcategoryid').empty()


        $.getJSON("http://localhost:8000/fetch_all_json",{categoryid:$('#categoryid').val()},function (data){
  //     alert(JSON.stringify(data))
        $('#subcategoryid').append($("<option>").text('Select SubCategory'))

//alert(1)
        var records=data.subdata


        records.map((item)=>{

            $('#subcategoryid').append($("<option>").text(item.subcategoryname).val(item.subcategoryid))
        })
        $('select').formSelect();
        })
    })

   $('#subcategoryid').change(function () {

        $('#brandid').empty()
        $('#brandid').append($("<option>").text('Select'))

        $.getJSON("http://localhost:8000/fetch_all_brand", { categoryid: $('#categoryid').val(),subcategoryid: $('#subcategoryid').val() }, function (data) {

            var record = data.bdata
            alert(JSON.stringify(record))
            record.map((item)=> {

                $('#brandid').append($("<option>").text(item.brandname).val(item.brandid))
            })
            $('select').formSelect();
        })
    })

    $('#brandid').change(function () {
        $('#productid').empty()
        $('#productid').append($("<option>").text('Select'))

        $.getJSON("http://localhost:8000/fetchallproductsjson", { brandid: $('#brandid').val() }, function (data) {
            var records = data.pdata

            records.map((item) => {

                $('#productid').append($("<option>").text(item.productname).val(item.productid))
            })
            $('select').formSelect();
        })
    })



})