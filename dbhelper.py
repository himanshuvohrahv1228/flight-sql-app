import mysql.connector

class DB:
    def __init__(self):
        #connect to database
        try:
            self.conn = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='',
                database='flights'
            )
            self.mycursor = self.conn.cursor()
            print('Connection Successful')
        except:
            print('Connection Error')

    def fetch_city_names(self):
        city = []
        self.mycursor.execute("""
        SELECT DISTINCT(Source) FROM flights.flights
        UNION
        SELECT DISTINCT(Destination) FROM flights.flights""")

        data = self.mycursor.fetchall()
        print(data)

        for item in data:
            city.append(item[0])
        return city

    def fetch_all_flights(self,source,destination):

        self.mycursor.execute("""
        SELECT Airline,Route,Dep_Time,Arrival_Time,Duration,Price FROM flights
        WHERE Source = '{}' AND Destination = '{}'
        """.format(source,destination))

        data = self.mycursor.fetchall()
        return data

    def fetch_airline_freq(self):
        airline = []
        freq = []

        self.mycursor.execute("""
        SELECT Airline,COUNT(*) FROM flights
        GROUP BY Airline
        """)

        data = self.mycursor.fetchall()
        for item in data:
            airline.append(item[0])
            freq.append(item[1])

        return airline,freq

    def busy_airport(self):
        city = []
        freq1 = []

        self.mycursor.execute("""
        SELECT Source,COUNT(*) FROM (SELECT Source FROM flights
							UNION ALL
                            SELECT Destination FROM flights) t
        GROUP BY t.Source
        ORDER BY COUNT(*) DESC
        """)

        data = self.mycursor.fetchall()
        for item in data:
            city.append(item[0])
            freq1.append(item[1])
        return city, freq1

    def daily_freq(self):
        date = []
        freq2 = []

        self.mycursor.execute("""
        SELECT date_of_journey, COUNT(*) FROM flights
        GROUP BY date_of_journey
        ORDER BY date_of_journey ASC
        """)

        data = self.mycursor.fetchall()
        for item in data:
            date.append(item[0])
            freq2.append(item[1])
        return date, freq2

    def flight_bw_cities(self):
        source = []
        destination = []
        freq = []

        self.mycursor.execute("""
        SELECT Source, Destination, COUNT(*) AS Flights
        FROM flights
        GROUP BY Source, Destination
        """)

        data = self.mycursor.fetchall()

        for item in data:
            source.append(item[0])  # Source city
            destination.append(item[1])  # Destination city
            freq.append(item[2])  # Flight count

        return source, destination, freq

    def cheapest_flight(self, source, destination):
        self.mycursor.execute("""
            SELECT Airline, Price
            FROM flights
            WHERE Source=%s AND Destination=%s
            ORDER BY Price ASC
            LIMIT 1
        """, (source, destination))

        return self.mycursor.fetchone()

    def fastest_flight(self, source, destination):
        self.mycursor.execute("""
            SELECT Airline, Duration
            FROM flights
            WHERE Source=%s AND Destination=%s
            ORDER BY Duration ASC
            LIMIT 1
        """, (source, destination))
        return self.mycursor.fetchone()

