import streamlit as st
import random

# =========================
# Vehicle Classes
# =========================
class Vehicle:
    def __init__(self, vid, name, speed, battery=100):
        self.id = vid
        self.name = name
        self.speed = speed
        self.battery = battery
        self.status = "idle"

    def move(self, distance):
        if self.battery <= 10:
            return f"{self.name} cannot move — low battery!"
        self.battery -= distance
        self.status = "working"
        return f"{self.name} moved {distance} km"

    def charge(self, amount):
        self.battery = min(100, self.battery + amount)
        self.status = "charging"
        return f"{self.name} charged"

    def info(self):
        return f"{self.id} | {self.name} | {self.battery:.1f}% | {self.status}"


class GroundVehicle(Vehicle):
    def __init__(self, vid, name, speed, terrain):
        super().__init__(vid, name, speed)
        self.terrain = terrain

    def move(self, distance):
        if self.battery <= 10:
            return f"{self.name} cannot move — low battery!"
        self.battery -= distance * 0.8
        self.status = "working"
        return f"{self.name} drove on {self.terrain}"


class Drone(Vehicle):
    def __init__(self, vid, name, speed, altitude):
        super().__init__(vid, name, speed)
        self.altitude = altitude

    def move(self, distance):
        if self.battery <= 15:
            return f"{self.name} cannot fly — low battery!"
        self.battery -= distance * 1.5
        self.status = "working"
        return f"{self.name} flew at {self.altitude}m"


class UGV(Vehicle):
    def __init__(self, vid, name, speed, capacity):
        super().__init__(vid, name, speed)
        self.capacity = capacity

    def deliver(self, weight):
        if weight > self.capacity:
            return f"{self.name} cannot carry that weight!"
        if self.battery <= 20:
            return f"{self.name} low battery!"
        self.battery -= weight * 2
        self.status = "working"
        return f"{self.name} delivered {weight}kg"