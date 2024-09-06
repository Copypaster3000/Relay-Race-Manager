# Relay Race Manager

This project simulates a dynamic, multi-leg relay race, managing athletes and estimating race completion times. The program uses a custom 2-3 tree data structure to organize race legs of various types, such as flat, steep, and trail. Despite the differences in race leg types, the tree handles multiple data types seamlessly, allowing for uniform code to estimate athletes' race leg times.

## Features

- Dynamic Data Handling with a 2-3 Tree: The program uses a flexible 2-3 tree to manage race legs of different types, such as flat, steep, and trail, allowing seamless handling of multiple data types. This structure optimizes the insertion, deletion, and search operations while maintaining the same code for different race leg types.
- Uniform Race Leg Time Estimation: Regardless of the specific leg type, the program uses the same lines of code to estimate each athlete's race leg time. This is achieved by leveraging Python’s dynamic typing and the 2-3 tree’s ability to handle different objects without modifying the algorithm.
- Object-Oriented Design with Inheritance: Classes for athletes, race legs, and specialized race leg types (e.g., flat, steep, trail) are built using inheritance, making the program highly modular, reusable, and scalable.
- Real-Time Race Simulation: The program dynamically tracks athlete performance, adjusting estimated future race leg times with custom time estimation algorithms by comparing the athlete's last actual race leg time with the give the race legs attributes and computing their average flat running speed to estimate their future race leg times
- Comprehensive Unit Testing: Thoroughly tests the core hierarchy, including the unique and shared functions of race legs, the functionality of the 2-3 tree, and exception handling for both.
