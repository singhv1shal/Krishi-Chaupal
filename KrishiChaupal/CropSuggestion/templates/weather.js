$(document).ready(function(){
  getDate();
  getCurrentLocation();
  getCurrentWeather();
}); // End of Doc Ready

// Display Current Date
function getDate (){
  var d = new Date();
  var days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
  var month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  var dd = d.getDate();
  if (dd == 1|| dd == 21 || dd == 31){
    dd = "st";
  }
  else if (dd == 2|| dd == 22){
    dd = "nd";
  }
  else if (dd == 3 || dd == 23){
    dd = "rd";
  }
  else{
    dd = "th";
  };
  
  var  dateString = days[d.getDay()] + " " + d.getDate() + dd + " " + month[d.getMonth()] + " " + d.getFullYear();
  document.getElementById("currentDate").innerHTML = dateString;
};


//Get Current City details
function getCurrentLocation () {
  
  // Get Location of user.  
  navigator.geolocation.getCurrentPosition(function(position) {
    var latitude = (position.coords.latitude);
    var longitude = (position.coords.longitude);
    var googleApi = ("https://maps.googleapis.com/maps/api/geocode/json?latlng=" + latitude + "," + longitude + "&key="+"AIzaSyA9BLLbrQvu_NsqNNaqc9waFPycSmhAFeI");
  
    //Ajax req to google for city & country
    $.getJSON(googleApi, function (response){
      console.log(response.results[0])
      var city = response.results[0].address_components[3].long_name;
      var country = response.results[0].address_components[5].short_name;
      $("#currentLoc").append(city+ ", " + country);
    });
  });
};
  
      
// **************Start of Current Forecast Function*****************
function getCurrentWeather(){
  // Get Location of user.  
  navigator.geolocation.getCurrentPosition(function(position) {
    var latitude = (position.coords.latitude);
    var longitude = (position.coords.longitude);
    var latLon = latitude+","+longitude;
    var proxy = "https://cors-anywhere.herokuapp.com/";
    var URL = "https://api.darksky.net/forecast/";
    var key = "de6331a13c6817a21cbb0646dbd6bd51/";
    var units = "?units=si";
   
    // Ajax request to weather API
    $.getJSON(proxy+URL+key+latLon+units, function(response) {
      
//*****************Main Current Weather Widget************************************** 
      // Current Text Summary
      var currentSummary = response.currently.summary;
      $("#currentDesc").append(currentSummary);
      
      //Current Temperature Cel/Fah
      var currentTempCel = Math.floor(response.currently.temperature);
      var currentTempFah = Math.floor((currentTempCel*1.8)+32);
      $("#currentTemp").html(currentTempCel+"<i class='wi wi-degrees'></i>");
      
      //Current Weather Icon 
      var currentIcon = response.currently.icon;
      switch(currentIcon) {
        case "clear-day":
          $("#currentIcon").append("<i class='wi wi-day-sunny'></i>");
          break;
        case "clear-night":
          $("#currentIcon").append("<i class='wi wi-night-clear'></i>");
          break;
        case "rain":
          $("#currentIcon").append("<i class='wi wi-day-rain'></i>");
          break;
        case "snow":
          $("#currentIcon").append("<i class='wi wi-day-snow-wind'></i>");
          break;
        case "sleet":
          $("#currentIcon").append("<i class='wi wi-day-sleet'></i>");
          break;
        case "wind":
          $("#currentIcon").append("<i class='wi wi-day-cloudy-gusts'></i>");
          break;
        case "fog":
          $("#currentIcon").append("<i class='wi wi-day-fog'></i>");
          break;
        case "cloudy":
          $("#currentIcon").append("<i class='wi wi-day-cloudy'></i>");
          break;
        case "partly-cloudy-day":
          $("#currentIcon").append("<i class='wi wi-day-cloudy'></i>");
          break;
        case "partly-cloudy-night":
          $("#currentIcon").append("<i class='wi wi-night-alt-cloudy'></i>");
          break;
        default:
          $("#currentIcon").append("<i class='wi wi-day-cloudy'></i>");
      };
      
//**********************Detailed Daily Weather Summary***********************
      
      // Detailed Temperature Max & Min
      var detTempMinCel = Math.floor(response.daily.data[0].temperatureMin);
      var detTempMinFah = Math.floor((detTempMinCel *1.8) + 32);
      var detTempMaxCel = Math.floor(response.daily.data[0].temperatureMax);
      var detTempMaxFah = Math.floor((detTempMaxCel*1.8) +32);
      $("#detMin").html("Min "+detTempMinCel+"<i class='wi wi-degrees'></i>");
      $("#detMax").html("Max "+detTempMaxCel+"<i class='wi wi-degrees'></i>");
      
      // Detailed Sunrise Time
      function getSunrise (){
        var riseTime = new Date((response.daily.data[0].sunriseTime)*1000);
        var detSunrise = "0"+ (riseTime.getHours()) + ":" + (riseTime.getMinutes());   
        $("#detSunrise").append(detSunrise);
      };
      getSunrise();
      
      // Detailed Sunset Time
      function getSunset (){
        var setTime = new Date((response.daily.data[0].sunsetTime)*1000);
        var detSunset = (setTime.getHours()) + ":" + (setTime.getMinutes());   
        $("#detSunset").append(detSunset);
      };
      getSunset();
      
      // Detailed Wind Speed & Direction
      var detWindSpeed = Math.floor((response.currently.windSpeed*2.23694));//JSON is in MetersPerSecond. Convert to miles
      var detWindDir = response.currently.windBearing;
      $("#detWindSpeed").append(detWindSpeed+" mph");
         // switch statement for WindDirection Icon
      if (detWindDir <22.5 || detWindDir > 337.5) {
        $("#detWindDir").append("<i class='wi wi-direction-down'></i>");
      } else if (detWindDir >22.5 && detWindDir <= 67.5) {
        $("#detWindDir").append("<i class='wi wi-direction-down-left'></i>");
      } else if (detWindDir >67.5 && detWindDir <= 112.5) {
        $("#detWindDir").append("<i class='wi wi-direction-left'></i>");
      } else if (detWindDir >112.5 && detWindDir <= 157.5) {
        $("#detWindDir").append("<i class='wi wi-direction-up-left'></i>");  
      } else if (detWindDir >157.5 && detWindDir <= 202.5) {
        $("#detWindDir").append("<i class='wi wi-direction-up'></i>"); 
      } else if (detWindDir >202.5 && detWindDir <= 247.5) {
        $("#detWindDir").append("<i class='wi wi-direction-up-right'></i>");  
      } else if (detWindDir >247.5 && detWindDir <= 292.5) {
        $("#detWindDir").append("<i class='wi wi-direction-right'></i>");  
      } else if (detWindDir >292.5 && detWindDir <= 337.5) {
        $("#detWindDir").append("<i class='wi wi-direction-down-right'></i>");   
      } else {
        $("#detWindDir").append("<i class='wi wi-windy'></i>");  
      };
      
      //Detailed Rain amount and probability
      var detRain = Math.floor(response.currently.precipIntensity);
      var detRainProb = Math.floor((response.currently.precipProbability)*100);
      $("#detRain").append(detRain+"mm");
      $("#detRainProb").append("Probability "+detRainProb+"%");
      
      //Detailed Cloud cover %   
      var detCloudCover = Math.floor((response.currently.cloudCover)*100);
      $("#detCloudCover").append(detCloudCover+"%");
      
      //Detailed Humidity %
      var detHumidity = Math.floor((response.currently.humidity)*100);
      $("#detHumidity").append(detHumidity+"%");

//*******************************Start of Hourly Summary **********************************
      // Get times for each column
      function getHourlyTimes() {
        for (var i=0; i<=11; i++) {
          var time = new Date((response.hourly.data[i].time)*1000);
          var hours = (time.getHours());
          var str = i.toString();
          $("#hourlyTime"+str).append(hours);
        };
      };
      getHourlyTimes();
      
      //Get Celsius Temperature for each column
      function getHourlyCelsius(){
        for (var i=0; i<=11; i++) {
          var temp = Math.floor(response.hourly.data[i].temperature);
          var str = i.toString();
          $("#hourlyTemp"+str).html(temp+"<i class='wi wi-degrees'></i>");
        };
      };
      getHourlyCelsius();
      
      //Get Fahrenheit Temperature for each column
      function getHourlyFah(){
        for (var i=0; i<=11; i++) {
          var temp = (response.hourly.data[i].temperature);
          var fahTemp = Math.floor((temp*1.8)+32);
          var str = i.toString();
          $("#hourlyTemp"+str).html(fahTemp+"<i class='wi wi-degrees'></i>");
        };
      };

      //Hourly Icon for each column
      function getHourlyIcon () {
        for (var i=0; i<=11; i++){       
          var currentIcon = response.hourly.data[i].icon;
          var str = i.toString();
          var ID = "#hourlyIcon"+str;
          
          switch(currentIcon) {
            case "clear-day":
              $(ID).append("<i class='wi wi-day-sunny'></i>");
              break;
            case "clear-night":
              $(ID).append("<i class='wi wi-night-clear'></i>");
              break;
            case "rain":
              $(ID).append("<i class='wi wi-day-rain'></i>");
              break;
            case "snow":
              $(ID).append("<i class='wi wi-day-snow-wind'></i>");
              break;
            case "sleet":
              $(ID).append("<i class='wi wi-day-sleet'></i>");
              break;
            case "wind":
              $(ID).append("<i class='wi wi-day-cloudy-gusts'></i>");
              break;
            case "fog":
              $(ID).append("<i class='wi wi-day-fog'></i>");
              break;
            case "cloudy":
              $(ID).append("<i class='wi wi-day-cloudy'></i>");
              break;
            case "partly-cloudy-day":
              $(ID).append("<i class='wi wi-day-cloudy'></i>");
              break;
            case "partly-cloudy-night":
              $(ID).append("<i class='wi wi-night-alt-cloudy'></i>");
              break;
            default:
              $(ID).append("<i class='wi wi-day-cloudy'></i>");   
          };  
        };  
      };
      getHourlyIcon();
      
//**********************Start of Daily 5 Forecast***************************************************
      
      // Get Days for each pill
      function getDays() {
        for (var i=0; i<=4; i++) {
          var date = new Date((response.daily.data[i].time)*1000);
          var day = date.getDay();
          var str = i.toString();
          var weekdays = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
          $("#day"+str).append(weekdays[day]);
        };
      };
      getDays();
      
      //Get Weather Summary for each Day
      function getDailySummary(){
        for (var i=0; i<=4; i++) {
          var summary = response.daily.data[i].summary;
          var str = i.toString();
          $("#daySummary"+str).append(summary);
        };
      };
      getDailySummary();
      
      
       //Get Celsius Min and Max Temperature for each Day
      function getDailyCelsius(){
        for (var i=0; i<=4; i++) {
          var minTemp = Math.floor(response.daily.data[i].temperatureMin);
          var maxTemp = Math.floor(response.daily.data[i].temperatureMax);
          var str = i.toString();
          $("#dayMin"+str).html("Min "+minTemp+"<i class='wi wi-degrees'></i>");
          $("#dayMax"+str).html("Max "+maxTemp+"<i class='wi wi-degrees'></i>");
        };
      };
      getDailyCelsius();
      
       //Get Celsius Temperature for each Day
      function getDailyFahrenheit(){
        for (var i=0; i<=4; i++) {
          var minTemp = (response.daily.data[i].temperatureMin);
          var maxTemp = (response.daily.data[i].temperatureMax);
          var minFah = Math.floor((minTemp*1.8)+32);
          var maxFah = Math.floor((maxTemp*1.8)+32);
          var str = i.toString();
          $("#dayMin"+str).html("Min "+minFah+"<i class='wi wi-degrees'></i>");
          $("#dayMax"+str).html("Min "+maxFah+"<i class='wi wi-degrees'></i>");
        };
      };
      
      // Daily Sunrise Time
      function getDailySunrise (){
        for(var i=0; i<=4; i++) {
          var riseTime = new Date((response.daily.data[i].sunriseTime)*1000);
          var daySunrise = "0"+ (riseTime.getHours()) + ":" + (riseTime.getMinutes());  
          var str = i.toString();
          $("#daySunrise"+str).append(daySunrise);
        };
      };
      getDailySunrise();
      
      // Daily Sunset Time
      function getDailySunset (){
        for(var i=0; i<=4; i++) {
          var setTime = new Date((response.daily.data[i].sunsetTime)*1000);
          var daySunset = (setTime.getHours()) + ":" + (setTime.getMinutes());  
          var str = i.toString();
          $("#daySunset"+str).append(daySunset);
        };
      };
      getDailySunset();
      
      // Daily Wind Speed 
      function getDailyWindSpeed (){
        for(var i=0; i<=4; i++) {
          var dayWindSpeed = Math.floor((response.daily.data[i].windSpeed*2.23694));//JSON is in MetersPerSecond. 
          var str = i.toString();
          $("#dayWindSpeed"+str).append(dayWindSpeed + " mph");
        };
      };
      getDailyWindSpeed();
      
      //Daily Wind Direction
      function getDailyWindDir () {
        for (var i=0; i<=4; i++){
          var dayWindDir = response.daily.data[i].windBearing;
          var str = i.toString();
          // switch statement for WindDirection Icon
          if (dayWindDir <22.5 || dayWindDir > 337.5) {
            $("#dayWindDir"+str).append("<i class='wi wi-direction-down'></i>");
          } else if (dayWindDir >22.5 && dayWindDir <= 67.5) {
            $("#dayWindDir"+str).append("<i class='wi wi-direction-down-left'></i>");
          } else if (dayWindDir >67.5 && dayWindDir <= 112.5) {
            $("#dayWindDir"+str).append("<i class='wi wi-direction-left'></i>");
          } else if (dayWindDir >112.5 && dayWindDir <= 157.5) {
            $("#dayWindDir"+str).append("<i class='wi wi-direction-up-left'></i>");  
          } else if (dayWindDir >157.5 && dayWindDir <= 202.5) {
            $("#dayWindDir"+str).append("<i class='wi wi-direction-up'></i>"); 
          } else if (dayWindDir >202.5 && dayWindDir <= 247.5) {
            $("#dayWindDir"+str).append("<i class='wi wi-direction-up-right'></i>");  
          } else if (dayWindDir >247.5 && dayWindDir <= 292.5) {
            $("#dayWindDir"+str).append("<i class='wi wi-direction-right'></i>");  
          } else if (dayWindDir >292.5 && dayWindDir <= 337.5) {
            $("#dayWindDir"+str).append("<i class='wi wi-direction-down-right'></i>");   
          } else {
            $("#dayWindDir"+str).append("<i class='wi wi-windy'></i>");  
          };
        };
      };
      getDailyWindDir();
      
      //Daily Rain & Probability
      function getDailyRain (){
        for (var i=0; i<=4; i++){
          var dayRain = Math.floor(response.daily.data[i].precipIntensity);
          var dayRainProb = Math.floor((response.daily.data[i].precipProbability)*100);
          var str = i.toString();
          $("#dayRain"+str).append(dayRain+"mm");
          $("#dayRainProb"+str).append(dayRainProb+"%");
        };
      };
      getDailyRain();
         
      //Daily Icon for each Pill
      function getDailyIcon () {
        for (var i=0; i<=4; i++){       
          var dailyIcon = response.daily.data[i].icon;
          var str = i.toString();
          var ID = "#dailyIcon"+str;
          
          switch(dailyIcon) {
            case "clear-day":
              $(ID).append("<i class='wi wi-day-sunny'></i>");
              break;
            case "clear-night":
              $(ID).append("<i class='wi wi-night-clear'></i>");
              break;
            case "rain":
              $(ID).append("<i class='wi wi-day-rain'></i>");
              break;
            case "snow":
              $(ID).append("<i class='wi wi-day-snow-wind'></i>");
              break;
            case "sleet":
              $(ID).append("<i class='wi wi-day-sleet'></i>");
              break;
            case "wind":
              $(ID).append("<i class='wi wi-day-cloudy-gusts'></i>");
              break;
            case "fog":
              $(ID).append("<i class='wi wi-day-fog'></i>");
              break;
            case "cloudy":
              $(ID).append("<i class='wi wi-day-cloudy'></i>");
              break;
            case "partly-cloudy-day":
              $(ID).append("<i class='wi wi-day-cloudy'></i>");
              break;
            case "partly-cloudy-night":
              $(ID).append("<i class='wi wi-night-alt-cloudy'></i>");
              break;
            default:
              $(ID).append("<i class='wi wi-day-cloudy'></i>");   
          };  
        };  
      };
      getDailyIcon();
     
      
//*******************************Fahrenheit to Celsius Switch Buttons***********************      
     //Fahrenheit Button
      $("#fahrenheitBtn").click(function(){
        $("#currentTemp").fadeOut('slow', function(){
          $("#currentTemp").html(currentTempFah+"<i class='wi wi-degrees'></i>");
        });
        $("#currentTemp").fadeIn('slow');
        $("#detMin").html("Min "+detTempMinFah+"<i class='wi wi-degrees'></i>");
        $("#detMax").html("Max "+detTempMaxFah+"<i class='wi wi-degrees'></i>"); 
        getHourlyFah();
        getDailyFahrenheit();
      });
        
      //Celsius Button
      $("#celsiusBtn").click(function(){
        $("#currentTemp").fadeOut('slow', function(){
          $("#currentTemp").html(currentTempCel+"<i class='wi wi-degrees'></i>");
        });
        $("#currentTemp").fadeIn('slow');
        $("#detMin").html("Min "+detTempMinCel+"<i class='wi wi-degrees'></i>");
        $("#detMax").html("Max "+detTempMaxCel+"<i class='wi wi-degrees'></i>");
        getHourlyCelsius();
        getDailyCelsius();
      });       
      
      
      
    }); //close JSON Req
  }); //close Navigator func
}; //close getCurrentWeather