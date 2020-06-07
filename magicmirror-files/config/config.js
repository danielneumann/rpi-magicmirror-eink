var config = {
  port: 8080,
  address: "0.0.0.0",
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
      position: "top_right",
      config: {
        location: "Cologne, DE",
        locationID: "2886242",
        appid: "ef086543063192ed65649a824d41e658"
      }
    },
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
      header: "Termine",
      position: "bottom_bar",
      config: {
        maximumEntries: 10,
        maxTitleLength: 40,
        fetchInterval: 3600000, // every 60 min
        animationSpeed: 0,
        fade: false,
        dateFormat: "DD.MM. HH:MM",
        fullDayEventDateFormat: "DD.MM.",
        timeFormat: "absolute",
        urgency: 7,
        wrapEvents: true,
        displayRepeatingCountTitle: false,
        calendars: [
          {
            symbol: "calendar-check-o",
            url: "https://calendar.google.com/calendar/ical/mail.danielkerrin%40gmail.com/private-5585ec0c8e7d82199f6f652e94973d26/basic.ics"
          }
        ]
      }
    },
  ]
};

/*************** DO NOT EDIT THE LINE BELOW ***************/
if (typeof module !== "undefined") {module.exports = config;}
