# cs7ns6-groupwork

TCD CS7NS6 Distributed Systems Exercise 2

## Introduciton

This project aim to implement a 。。。。

## Requirements

We need to implement a global-oriented journey management system that allows drivers to book/cancel journeys. According to the requirement, all road-vehicle drivers are required to prebook every journey that they wish to make, no driver is allowed to start a journey without having received a notification that the requested journey is acceptable.

These require us to provide a high-performance service, it has to meet at least the following requirements (The focus of our system implementation exercise is not the business logic of journey management) :

* This service needs to be scalable. (All journeys required a prebook, the number of users might be very large.)

* The service needs to be highly available. (No driver is allowed to start a journey without having received a notification)

* The service needs to be reliable. (Before starting the journey, the drivers receive a notification that the requested journey is acceptable)

  

  #### Functional requirements-API

  -- prebook_journey(driverId)

  ~~-- confirmJourney(driverId, orderId)~~

  ~~-- startJourney(driverId, orderId)~~

  -- cancel_journey(driverId, orderId)

  -- get_journey(driverId)

  

  #### Non-functional requirements

  | Scale               | **1M/s** |
  | :------------------ | -------- |
  | **I/O performance** | **ms**   |
  | **scalability**     | **..**   |
  | **availability**    | **..**   |
  | **reliability**     | **..**   |
  |                     |          |

  

  

  

## Specifications

- 

## Architecture