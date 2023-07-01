$(document).ready(function () {

    var hashes = window.location.href.slice(window.location.href.indexOf('?')+ 1)
    // alert(hashes)
    var i=hashes.indexOf(":")+1
    var j=hashes.indexOf(",")
    // alert(i+","+j)
    var pid=hashes.slice(i,j)


     $.getJSON('/Fetch_cart',function (data) {
             // alert(data.data)
              var cart=JSON.parse(data.data)

              var key=Object.keys(cart)

              $('#shoppingcart').html(`( ${key.length} Articals)  &nbsp;&nbsp;`)
            if(key.includes(pid)) {
           $('.addtocart').hide()
                 $('#qtycomponent').show()

            $('#qnty').html(cart[pid]['qnty'])
   }else{
                 $('#qtycomponent').hide()
            }

    })

    $('#qtycomponent').hide()
    $.getJSON('http://localhost:8000/fetch_all_category_user',function (data) {

        var htm=''
       data.data.map((item)=>{
            htm+= `<li><a href="#">${item.categoryname}</a></li>`
        })
        $(".mainmenu").html(htm)
        })

    $.getJSON('http://localhost:8000/fetch_all_Product_user',function (data) {
        htm=" "
        data.data.map(item=>{
            var price
            var offerprice
            var save

            if(item.offerprice>0)
            {  price="<s style='color: red;'>"+item.price+"</s>"
                offerprice=item.offerprice
                save=item.price-item.offerprice
            }
            else
        {
            offerprice = item.price
            price = "<div> </div>"
            save = "<div> </div>"
        }
            var data=JSON.stringify(item)
            htm+=`<a href='http://localhost:8000/Buy_product?product=${data}'>
                     <div style="border-radius: 10px; margin:20px; width: 250px;height:auto;padding:5px;border: 1px solid #95a5a6;
                        display: flex;align-items: center;flex-direction: column;box-shadow: 1px 1px 3px #bdc3c7;elevation: below;background: #ffffff">
                     <div>
                           <img src="http://localhost:8000/static/${item.productimage}" style=" width:150px; height: 150px">
            </div>
            
            <div style="padding: 5px;">
            
            <div style="width: 200px;font-weight:bold;text-align: left;color: black">
                          ${item.productname}  
                     <div style="font-weight: initial;font-size: 15px;color: #01a3a4;background: #f1f2f6;display: flex;justify-content: space-between;font-variant: small-caps;">${item.scname}
                     <span style="color:#0984e3;">${item.cname}</span>
                     </div>
             
              </div>
            </div>
            
            <div style="width: 200px;font-size:14px;color: #636e72;">
               <i>Mkt: ${item.bname}</i>
             </div>
            
            <div style="width:200px;color: #636e72;">
              MRP* <span style="color: #ef5350">&#8377  ${price}</span>
             </div>
             
               <div style="width:200px ;color: #636e72;">
                Offer* <span style="color: crimson">&#8377 ${offerprice}</span>
             </div>
             
               <div style="width:200px;color: green">
                <i>You Save &#8377 ${save}</i>
             </div>
            </div> </a>`
        })

        $('#productlist').html(htm)
    })

      $.getJSON('http://localhost:8000/fetch_all_Subcategory_user',function (data) {
          var htm=' '
          data.data.map(item=>{
              htm+=`<div style="margin:5px;padding:10px;width: 310px;background:#ffffff ;height:80px;border-radius:10px;display:flex;flex-direction:row;"> `
              htm+=`<div style="padding:5px;"><img src="/static/${item.subcategoryicon}" width="40"></div>`
              htm+=`<div style="display: flex;flex-direction: column;"><div style="font-weight: bold; padding: 5px;">${item.subcategoryname}</div><div style="color: green">  Save upto 15%</div></div>`
              htm+=`</div>`
          })

          $('#subcategorylist').html(htm)
      })


    $('.plus').click(function () {
        var v=$('#qnty').html()
        if(v<=4)
        v++
        $('#qnty').html(v)
        Cartcontainer($(this).attr('product'),  $('#qnty').html())

    })


    $('.remove').click(function () {

        var k=$('#qnty').html()
        if(k>0)
        k--
        if(k==0){
             $('.addtocart').show()
             $('#qtycomponent').hide()
            // alert($(this).attr('productid'))
            RemoveCartcontainer($(this).attr('productid'))
        }
        else {
            $('#qnty').html(k)
            Cartcontainer($(this).attr('product'), $('#qnty').html())
        }
    })

    $('.addtocart').click(function () {
          $('.addtocart').hide()
          $('#qtycomponent').show()
          $('#qnty').html(1)
        Cartcontainer($(this).attr('product'),  $('#qnty').html())

})


    function Cartcontainer(product,qnty) {

          $.getJSON('/add_to_cart',{'product':product,'qnty':qnty},function (data) {
             // alert(data.data)
            var cart=JSON.parse(data.data)

              var key=Object.keys(cart)

              $('#shoppingcart').html(`( ${key.length} Articals) &nbsp; &nbsp;`)
    })
    }

     function RemoveCartcontainer(productid) {

             $.getJSON('/remove_from_cart',{'productid':productid},function (data) {
                // alert('removed')
                 var cart=JSON.parse(data.data)

              var key=Object.keys(cart)

              $('#shoppingcart').html(`( ${key.length} Articals) &nbsp; &nbsp;`)
            })
             // alert(data.data)

    }
})