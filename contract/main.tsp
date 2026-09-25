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
    @get search(
      origin: string, 
      destination: string, 
      date: string, 
      passengers?: integer
    ): {
      @statusCode statusCode: 200;
      body: Flight[];
    } | {
      @statusCode statusCode: 400;
      body: ApiError;
    };
}

@route("/api/flights/{id}")
interface FlightId {
    @get find(id: string): {
        @statusCode statusCode: 200;
        body: Flight;
    } | {
        @statusCode statusCode: 404;
        body: ApiError;
    };
}

@route("/api/bookings")
interface Bookings {
    @post book(body: CreateBookingRequest): {
        @statusCode statusCode: 201;
        body: Booking;
    } | {
        @statusCode statusCode: 400;
        body: ApiError;
    };
}

@route("/api/bookings/{code}")
interface BookingCode {
    @get view(
      code: string, 
      lastName: string
      ): {
        @statusCode statusCode: 200;
        body: Booking;
    } | {
        @statusCode statusCode: 403;
        body: ApiError;
    } | {
        @statusCode statusCode: 404;
        body: ApiError;
    };
}

@route("/api/bookings/{code}/cancel")
interface BookingCancel {
    @post cancel(
      code: string, 
      body: CancelBookingRequest
      ): {
        @statusCode statusCode: 200;
        body: Booking;
    } | {
        @statusCode statusCode: 404;
        body: ApiError;
    };
}