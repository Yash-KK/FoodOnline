let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address_line'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['in']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();    

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address_line').placeholder = "Start typing...";
    }
    else{
        console.log('place name=>', place.name)
         // Fill the address_line field
         document.getElementById('id_address_line').value = place.formatted_address;

         // Fill the country field
         var country = place.address_components.find(function(component){
             return component.types.includes('country');
         });
         document.getElementById('id_country').value = country.long_name;
 
         // Fill the state field
         var state = place.address_components.find(function(component){
             return component.types.includes('administrative_area_level_1');
         });
         document.getElementById('id_state').value = state.long_name;
 
         // Fill the city field
         var city = place.address_components.find(function(component){
             return component.types.includes('locality') || component.types.includes('sublocality');
         });
         document.getElementById('id_city').value = city.long_name;
 
         // Fill the pincode field
         var pincode = place.address_components.find(function(component){
             return component.types.includes('postal_code');
         });
         document.getElementById('id_pincode').value = pincode.long_name;
 
         // Fill the latitude and longitude fields
         document.getElementById('id_latitude').value = place.geometry.location.lat();
         document.getElementById('id_longitude').value = place.geometry.location.lng();
    }
    // get the address components and assign them to the fields
}





$(document).ready(function(){    
    $('.add_to_cart').click(function(e){
        e.preventDefault();
        
        let food_id = $(this).data('id');
        let url = $(this).data('url');
        
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                if(response.login_required){
                    swal(response.login_required, "--", "error");
                } else{                    
                    
                    // Update tax data
                    updateTax(response);                   

                    // Update the item quantity
                    let quantity = response.quantity;
                    $("#qty-"+food_id).html(quantity);

                    // Update the cart count
                    let cart_count = response.cart_count;
                    $("#cart_counter").html(cart_count);
                }
            }
        });               
    })

    $(".decrease_cart").click(function(e){
        e.preventDefault();

        let food_id = $(this).data('id');
        let cart_id = $(this).data('cartid');

        let url = $(this).data('url');

        
        $.ajax({
            type:'GET',
            url:url,
            success: function(response){
                if(response.login_required){
                    swal(response.login_required, "--", "error");

                } else if (response.qty0){
                    swal(response.qty0, "--", "warning");
                } else {                                             

                    // Update tax data
                    updateTax(response);

                    // Update the cart count
                    let cart_count = response.cart_count;
                    $("#cart_counter").html(cart_count);

                    // Show empty cart message if cart count == 0
                    if(cart_count == 0){
                        $("#empty-cart").show();
                    }

                    // Update the item quantity
                    let quantity = response.quantity;
                    $("#qty-"+food_id).html(quantity);
 
                    if (window.location.href == 'http://127.0.0.1:8000/cart/'){
                        if (quantity == 0){
                            $("#cart-item-"+cart_id).remove();                            
                        }
                    }
                }

            }
        })
    });

    $('.delete_cart').click(function(e){
        e.preventDefault();
        
        let url = $(this).data('url');
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                if(response.login_required){
                    swal(response.login_required, "--", "error");
                } else{
                    

                    // Update tax data
                    updateTax(response);

                    // Remove the cart item
                    let cart_id = response.cart_id;
                    $("#cart-item-"+cart_id).remove();

                    swal("Cart Item deleted", '--', 'success');

                    // Update the cart count
                    let cart_count = response.cart_count;
                    $("#cart_counter").html(cart_count);

                    // Show empty cart message if cart count == 0
                    if(cart_count == 0){
                        $("#empty-cart").show();
                    }

                }
            }
        })

    })


    $('.cart_quantity').each(function(){
        let quantity = $(this).data('quantity');
        let food_id = $(this).data('foodid');

        $("#qty-"+ food_id).html(quantity);

    });

    function updateTax(response){
        subtotal = response.tax_data['subtotal'];
        tax = response.tax_data['tax'];
        grandtotal = response.tax_data['grandtotal'];

        $("#subtotal").html(subtotal);
        $("#tax").html(tax);
        $("#grandtotal").html(grandtotal);
    }

   
    // Opening Hour
    $('.add_hour').click(function(e){
        e.preventDefault();

        let day = document.getElementById('id_day').value;
        let from_hour = document.getElementById('id_from_hour').value;
        let to_hour = document.getElementById('id_to_hour').value;
        let is_closed = document.getElementById('id_is_closed').checked;

        let url = document.getElementById('add_hour_url').value;

        if (is_closed){            
            if(day !== ''){
                $.ajax({
                    type: 'POST',
                    url: url,
                    headers: {
                        'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
                    },
                    data: {
                        'day': day,
                        'from_hour': '',
                        'to_hour': '',
                        'is_closed': is_closed
                    },
                    success: function(response){
                        if(response.error){
                            swal(response.error,'--', 'warning')
                        } else{
                            let days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
                            let row = '<tr id="hour-' + response.id + '"> <td><b>' + days[response.day - 1] + '</b></td> <td>Closed</td> <td><a href="#" class="remove_hour" data-url="/vendor/remove-opening-hour/'+ response.id +'/">Remove</a></td> </tr>'
                            $(".opening_hours").append(row);
                        }

                    }
                })
            } else{
                swal('Please select the day!', '--', 'warning')
            }
        } else{           
            if(from_hour !== '' && to_hour !== '' && day != ''){
                $.ajax({
                    type: 'POST',
                    url: url,
                    headers: {
                        'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
                    },
                    data: {
                        'day': day,
                        'from_hour': from_hour,
                        'to_hour': to_hour,
                        'is_closed': is_closed
                    },
                    success: function(response){
                        if(response.error){
                            swal(response.error,'--', 'warning')
                        } else{
                            let days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
                            let row = '<tr id="hour-' + response.id + '"> <td><b>' + days[response.day - 1] + '</b></td> <td> '+ response.from_hour + ' - '+ response.to_hour +' </td> <td><a href="#" class="remove_hour" data-url="/vendor/remove-opening-hour/'+ response.id +'/">Remove</a></td> </tr>'
                            $(".opening_hours").append(row);
                            
                        }
                    }
                })
            } else{
                swal('Please fill all the fields!', '--', 'warning')
            }
        }
       
        $("#opening_hours").trigger('reset');
        
    })

    $(document).on("click", ".remove_hour", function(e) {
        e.preventDefault();
        let url = $(this).data('url');
       
        $.ajax({
            type: 'POST',
            url: url,
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response){               
                $("#hour-"+ response.hour_id).remove();

            }
        })
      });
   
    // End of JQuery
})