var config = {
  address: "localhost",
  port: 8080,
  ipWhitelist: [],
  language: "de",
  timeFormat: 24,
  units: "metric",
  modules: [
    {
      module: "calendar_monthly",
      position: "top_left",
      config: {
      }
    },
    {
      module: "MMM-weatherforecast",
      position: "top_right",	// This can be any of the regions.
            // Best results in bottom_bar region due to horizontal default layout and icon sizes.
      config: {
        // See 'Configuration options' for more information.
        location: "Cologne, DE",
        locationID: "2886242", //Location ID from http://openweathermap.org/help/city_list.txt
        appid: "ef086543063192ed65649a824d41e658" //openweathermap.org API key.
      }
    }
    {
      module: "currentweather",
      position: "top_right",
      config: {
        appendLocationNameToHeader: false,
        animationSpeed: 0,
        fade: false,
        location: "Cologne, DE",
        appid: "ef086543063192ed65649a824d41e658"
      }
    },
    {
      module: "clock",
      position: "middle_center",
      config: {
        showWeek: true,
        displaySeconds: false,
        showSunTimes: true,
        showMoonTimes: true,
        lat: "50.960061",
        lon: "6.980950"
      }
    },
    {
      module: "calendar",
      header: "Geburtstage",
      position: "bottom_bar",
      config: {
        maximumEntries: 10,
        maxTitleLength: 40,
        fetchInterval: 3600000, // every 60 min
        animationSpeed: 0,
        fade: false,
        dateFormat: "DD.MM.",
        fullDayEventDateFormat: "DD.MM.",
        timeFormat: "absolute",
        urgency: 7,
        wrapEvents: true,
        displayRepeatingCountTitle: false,
        calendars: [
          {
            symbol: "calendar-check-o",
            url: "webcal://www.calendarlabs.com/ical-calendar/ics/46/Germany_Holidays.ics"
          }
        ]
      }
    },
  ]
};

/*************** DO NOT EDIT THE LINE BELOW ***************/
if (typeof module !== "undefined") {module.exports = config;}
