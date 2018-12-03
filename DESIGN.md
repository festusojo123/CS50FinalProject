Design Document
“Moves” is your solution to every Friday night when you find yourself bored in your dorm room and want to ask “what’s the move?”. While implementing this web application, we first took the implementation of our C$50 Finance problem set, and stripped it of its major details. We changed the application icon that appears in the corner and changed a lot of the CSS details to give our app its own unique feel and look.
At first, we desired to display a custom calendar with events that users could add to. However, we learned this would require PHP. Professor Malan told us this would not be possible due to Flask’s functionality. After this, we embedded a Google calendar with a unique Google account so all of the events could be on one central calendar displayed on the index page. However, in order to allow users to add events to this calendar, we would have to use the Google calendar API which also would require PHP.
Moving on from this idea, we decided to simply allow users to see every event on the index or home page of our web application. However, to make this experience more user-friendly, we decided to divide up the functionality of initially registering a new event into our event catalogue and signing up for already existing events. In addition to this, by adding a button at the bottom of each index, there’s the ability for the user to add the event to their own personal Google calendar. Furthermore, users can search for a particular event by entering its name (should be unique) and then view everyone else attending that event. Other features we decided to include are the ability to search for events by accessing Google on the top right corner as well as pages where users can be redirected to Venmo, Uber, and Lyft, and be able to pay for a particular/split transportation costs (per their explicit permission on these 3rd party apps).