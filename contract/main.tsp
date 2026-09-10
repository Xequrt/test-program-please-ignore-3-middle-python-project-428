import "@typespec/http";

using TypeSpec.Http;

@service(#{ title: "Flight Booking API" })
namespace FlightBookingApi;

model City {
  code: string;
  name: string;
  country?: string;
}

model Money {
  amount: integer;
  currency: string;
}

model Airline {
    code: string;
    name: string;
}

model Flight {
    id: string;
    flightNumber: string;
    airline: Airline;
    origin: City;
    destination: City;
    departureAt: string;
    arrivalAt: string;
    durationMinutes: integer;
    price: Money;
    seatsAvailable: integer;
}

model Passenger {
    firstName: string;
    lastName: string;
    dateOfBirth: string;
    documentNumber: string;
}

model Contact {
    email: string;
    phone: string;
}

model Booking {
    code: string;
    status: string;
    flight: Flight;
    passengers: Passenger[];
    contact: Contact;
    totalPrice: Money;
    createdAt: string;
}

model ApiError {
    code: string;
    message: string;
}

model CreateBookingRequest {
    flightId: string;
    passengers: Passenger[];
    contact: Contact;
}

model CancelBookingRequest {
    lastName: string;
}

@route("/api/health")
interface Health {
  @get check(): { status: string };
}

@route("/api/cities")
interface Cities {
  @get list(): City[];
}

@route("/api/flights")
interface Flights {
    @responses(
      { statusCode: 200, type: Flight[] },
      { statusCode: 400, type: ApiError }
    )
    @get search(
      origin: string, destination: string, date: string, passengers?: integer
    ): Flight[];
}

@route("/api/flights/{id}")
interface FlightId {
    @responses(
      { statusCode: 200, type: Flight },
      { statusCode: 404, type: ApiError }
    )

     @get find(
       id: string
     ): Flight;
}

@route("/api/bookings")
interface Bookings {
    @responses(
      { statusCode: 201, type: Booking },
      { statusCode: 400, type: ApiError }
    )

    @post book(body: CreateBookingRequest): Booking
}

@route("/api/bookings/{code}")
interface BookingCode {
    @responses(
      { statusCode: 200, type: Booking },
      { statusCode: 403, type: ApiError },
      { statusCode: 404, type: ApiError }
    )

    @get view(code: string, lastName: string): Booking
}

@route("/api/bookings/{code}/cancel")
interface BookingCancel {
    @responses(
      { statusCode: 200, type: Booking },
      { statusCode: 404, type: ApiError }
    )

    @post cancel(code: string, body: CancelBookingRequest): Booking
}