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