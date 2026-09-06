import "@typespec/http";

using TypeSpec.Http;

@service(#{ title: "Flight Booking API" })
namespace FlightBookingApi;

model City {
  code: string;
  name: string;
  country?: string;
}

@route("/api/cities")
interface Cities {
  @get list(): City[];
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

@route("/api/health")
interface Health {
  @get check(): { status: string };
}