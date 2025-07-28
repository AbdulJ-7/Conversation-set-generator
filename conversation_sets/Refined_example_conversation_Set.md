# Revisions in this example conversation set:
## 1. Using multiple interdependent functions to satisfy every prompt
## 2. Using the booking.com tool so the conversation is built on a travel & tourism scenario.



### 1.  
>I want to plan a trip to London.Find me a highly-rated hotel, and then tell me about some popular attractions near it. Also, I'll need to rent a car, so find a car rental place near one of those attractions and check for the availability of a standard car for tomorrow for a day.  

**Tools:**  
1. `Search_Hotel_Destination`  
   - **Arguments:** `query: "London"`  
   - **Expected Output:**  
     ```json
     {
       "status": true,
       "message": "Success",
       "data": [
         {
           "dest_id": "-2601889",
           "dest_type": "city"
         }
       ]
     }
     ```
2. `Search_Hotels`  
   - **Arguments:** `dest_id: "-2601889", dest_type: "city", arrival_date: "2025-08-15", departure_date: "2025-08-17", sort_by: "popularity"`  
   - **Expected Output:**  
     ```json
     {
       "status": true,
       "message": "Success",
       "data": {
         "hotels": [
           {
             "hotel_id": "12345",
             "hotel_name": "The Ritz London",
             "latitude": 51.5074,
             "longitude": -0.1278
           }
         ]
       }
     }
     ```
3. `Get_Popular_Attraction_Near_By`  
   - **Arguments:** `hotel_id: "12345"`  
   - **Expected Output:**  
     ```json
     {
       "status": true,
       "message": "Success",
       "data": {
         "attractions": [
           {
             "attraction_id": "att789",
             "name": "Buckingham Palace",
             "latitude": 51.5014,
             "longitude": -0.1419
           },
           {
             "attraction_id": "att101",
             "name": "The British Museum",
             "latitude": 51.5194,
             "longitude": -0.127
           }
         ]
       }
     }
     ```
4. `Search_Car_Location`  
   - **Arguments:** `query: "Buckingham Palace"`  
   - **Expected Output:**  
     ```json
     {
       "status": true,
       "message": "Success",
       "data": [
         {
           "city": "London",
           "coordinates": {
             "longitude": -0.1419,
             "latitude": 51.5014
           },
           "country": "United Kingdom",
           "name": "Buckingham Palace"
         }
       ]
     }
     ```
5. `Search_Car_Rentals`  
   - **Arguments:**  
     ```json
     {
       "pick_up_latitude": 51.5014,
       "pick_up_longitude": -0.1419,
       "drop_off_latitude": 51.5014,
       "drop_off_longitude": -0.1419,
       "pick_up_date": "2025-07-29",
       "drop_off_date": "2025-07-30",
       "pick_up_time": "09:00",
       "drop_off_time": "09:00"
     }
     ```  
   - **Expected Output:**  
     ```json
     {
       "status": true,
       "message": "Success",
       "data": {
         "search_results": [
           {
             "vehicle_info": {
               "v_name": "Ford Focus"
             },
             "pricing_info": {
               "price": 75
             }
           }
         ]
       }
     }
     ```

### 2. 

>Tell me more about The Ritz London. What are its policies, what do the reviews say, what kind of rooms are available, and what are the payment options?

**Tools:**  
1. `Get_Hotel_Details`  
   - **Arguments:** `hotel_id: "12345"`  
   - **Expected Output:**  
     ```json
     {
       "status": true,
       "message": "Success",
       "data": {}
     }
     ```
2. `Get_Hotel_Policies`  
   - **Arguments:** `hotel_id: "12345"`  
   - **Expected Output:**  
     ```json
     {
       "status": true,
       "message": "Success",
       "data": {}
     }
     ```
3. `Get_Hotel_Reviews(Tips)`  
   - **Arguments:** `hotel_id: "12345"`  
   - **Expected Output:**  
     ```json
     {
       "status": true,
       "message": "Success",
       "data": {}
     }
     ```
4. `Get_Room_List`  
   - **Arguments:** `hotel_id: "12345"`  
   - **Expected Output:**  
     ```json
     {
       "status": true,
       "message": "Success",
       "data": {}
     }
     ```
5. `Payment_features_of_the_Hotel`  
   - **Arguments:** `hotel_id: "12345"`  
   - **Expected Output:**  
     ```json
     {
       "status": true,
       "message": "Success",
       "data": {}
     }
     ```

### 3.  
> Find me a flight from New York to London for the 14th of August, returning on the 20th. What's the cheapest flight available, and can you give me the details of a premium economy flight on those dates?

**Tools:**  
1. `Search_Flight_Location`  
   - **Arguments:** `query: "New York"`  
   - **Expected Output:**  
     ```json
     {
       "status": true,
       "message": "Success",
       "data": [
         {
           "iata": "JFK"
         }
       ]
     }
     ```
2. `Search_Flight_Location`  
   - **Arguments:** `query: "London"`  
   - **Expected Output:**  
     ```json
     {
       "status": true,
       "message": "Success",
       "data": [
         {
           "iata": "LHR"
         }
       ]
     }
     ```
3. `Search_Flights`  
   - **Arguments:**  
     ```json
     {
       "from_code": "JFK",
       "to_code": "LHR",
       "from_date": "2025-08-14",
       "to_date": "2025-08-20",
       "cabin_class": "premium_economy"
     }
     ```  
   - **Expected Output:**  
     ```json
     {
       "status": true,
       "message": "Success",
       "data": {
         "flights": [
           {
             "flight_id": "fl123",
             "price": 1200
           }
         ]
       }
     }
     ```
4. `Get_Min_Price`  
   - **Arguments:**  
     ```json
     {
       "from_code": "JFK",
       "to_code": "LHR",
       "from_date": "2025-08-14",
       "to_date": "2025-08-20"
     }
     ```  
   - **Expected Output:**  
     ```json
     {
       "status": true,
       "message": "Success",
       "data": {
         "price": 800
       }
     }
     ```
5. `Get_Flight_Details`  
   - **Arguments:** `flight_id: "fl123"`  
   - **Expected Output:**  
     ```json
     {
       "status": true,
       "message": "Success",
       "data": {}
     }
     ```

## 4.  
Tell me more about the British Museum. Also, search for other museums in London.  Can you find me a taxi from The Ritz London to the British Museum?

**Tools:**  
1. `Get_Attraction_Details`  
   - **Arguments:** `attraction_id: "att101"`  
   - **Expected Output:**  
     ```json
     {
       "status": true,
       "message": "Success",
       "data": {}
     }
     ```
2. `Search_Attraction_Location`  
   - **Arguments:** `query: "London"`  
   - **Expected Output:**  
     ```json
     {
       "status": true,
       "message": "Success",
       "data": {
         "location_id": "loc456"
       }
     }
     ```
3. `Search_Attractions`  
   - **Arguments:** `location_id: "loc456", category: "museums"`  
   - **Expected Output:**  
     ```json
     {
       "status": true,
       "message": "Success",
       "data": {}
     }
     ```
4. `Taxi_Search_Location`  
   - **Arguments:** `query: "The Ritz London"`  
   - **Expected Output:**  
     ```json
     {
       "status": true,
       "message": "Success",
       "data": {
         "latitude": 51.5074,
         "longitude": -0.1278
       }
     }
     ```
5. `Taxi_Search_Location`  
   - **Arguments:** `query: "The British Museum"`  
   - **Expected Output:**  
     ```json
     {
       "status": true,
       "message": "Success",
       "data": {
         "latitude": 51.5194,
         "longitude": -0.127
       }
     }
     ```
6. `Search_Taxi`  
   - **Arguments:**  
     ```json
     {
       "from_latitude": 51.5074,
       "from_longitude": -0.1278,
       "to_latitude": 51.5194,
       "to_longitude": -0.1270
     }
     ```  
   - **Expected Output:**  
     ```json
     {
       "status": true,
       "message": "Success",
       "data": {}
     }
     ```
