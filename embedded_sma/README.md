# Cooperative Multi-Agent System with BDI for ESP32/ESP8266

![Cooperation Demo](https://via.placeholder.com/800x400.png?text=Insert+a+GIF+of+the+Cooperation+here)
> **GIF Suggestion:** Showcase the sensor agent detecting darkness, the LED agent lighting up, and then the ultrasonic agent detecting an object, prompting the main agent's buzzer to sound.

This repository contains the implementation of a **Cooperative Multi-Agent System** using the **BDI (Beliefs, Desires, Intentions)** reasoning architecture. The agents, running on microcontrollers like the **ESP32** and **ESP8266**, form a distributed intelligence network capable of perceiving their environment and collaborating to achieve goals.

## Key Features

-   **Autonomous Reasoning (BDI)**: Each agent uses the BDI cycle to deliberate on its beliefs (what it knows about the world) and execute plans to achieve its goals.
-   **ESP-NOW Mesh Network**: Agents discover and communicate with each other efficiently and with low latency, without the need for a central router.
-   **Intelligent Cooperation**: Agents can request help and delegate tasks to others that possess the necessary capabilities (e.g., "turn on your LED," "sound your alarm").
-   **Hardware Heterogeneity**: The system supports different platforms (ESP32, ESP32-S3, ESP8266), each with its own set of sensors and actuators.
-   **Persistent Goal-Oriented Behavior**: Implementation of goal-driven logic that allows agents to maintain continuous behaviors until a specific condition is met.

## System Architecture

The system is composed of a network of independent agents. Communication is the backbone of the architecture, allowing the perceptions of one agent to trigger actions in another.

![Agent Network Diagram](https://via.placeholder.com/800x300.png?text=Agent+Network+Diagram)
> **Diagram Suggestion:** Draw nodes for each agent (`central-agent`, `led-agent`, `sonic-agent`). Connect them with arrows indicating "ESP-NOW Broadcast (Discovery)" and "ESP-NOW Unicast (Cooperation)".

## The Agents

The network currently consists of:

1.  **Central Agent (ESP32)**: The main "brain," equipped with multiple sensors (LDR, Potentiometer) and actuators (Buzzer). It can coordinate actions and respond to requests.
2.  **Actuator Agent (ESP32-S3)**: Specialized in acting upon the environment, primarily with a high-intensity LED.
3.  **Sonic Sensor Agent (ESP8266)**: A lightweight, low-cost agent focused on a single task: detecting object proximity with an ultrasonic sensor (HC-SR04).

## Development Journey & Roadmap

This section details the project's evolution and future objectives.

### ✅ Milestones

-   [x] **BDI Foundation**: Implemented the core reasoning cycle and basic plans.
-   [x] **ESP-NOW Communication**: Created a robust module for neighbor discovery and management.
-   [x] **Multi-Platform Expansion**: Ported the codebase to the **ESP8266**, creating the `sonic-agent` and validating cooperation between different hardware types.
-   [x] **Goal-Oriented Reasoning**: Implemented "recursive" plans that enable persistent behaviors, such as an alarm that sounds intermittently until deactivated.
-   [ ] **Multi-Hop Routing**: Allow agents to forward messages, creating a true mesh network where cooperation can occur even between agents that are not in direct range.
-   [x] **Capability Expansion**: Integrate new sensors (DHT11, LM35) and develop more complex use-case scenarios.
-   [x] **Network Resilience Testing**: Validate the system's ability to self-heal when agents leave and rejoin the network.
-   [ ] **Context-Based Plan Selection**: Implement multiple plans for the same trigger, allowing an agent to choose the best strategy based on a broader context (e.g., a power-saving mode).

## Design Patterns and Technical Solutions

In addition to classic patterns (Producer-Consumer, Observer, Command), this project employs two specific solutions to address the challenges of embedded and networked systems:

### 🎭 Bitmasking for Capability Broadcasting

To efficiently communicate what each agent can do, we use a **bitmask**. Instead of sending strings, a single byte can represent up to 8 distinct capabilities (e.g., `CAP_SENSOR_LIGHT`, `CAP_ACTUATOR_BUZZER`). The `|` (bitwise OR) operator is used to combine capabilities for sending, and the `&` (bitwise AND) operator is used to check for them, resulting in extremely lightweight network communication.

### 🎯 Goal-Oriented Recursive Plans

To create persistent behaviors (like an alarm that sounds until turned off), we use an advanced BDI pattern. An initial event (e.g., `+is_hot`) doesn't trigger an action directly, but rather a **goal** (e.g., `+!cool_down_room`). Multiple plans react to this goal:

1.  **The Looping Plan**: Executes the action (e.g., sounds the alarm) and, in its body, **re-posts its own goal**. This forces the agent to re-evaluate the intention in the next cycle, creating a loop.
2.  **The Exit Plan**: Has a context that represents the "success condition" (e.g., user intervention). When this plan is executed, the goal is achieved, and the loop is broken.

This enables the creation of complex, self-sustaining behaviors by leveraging the agent's continuous reasoning cycle.

## Hardware and Pinout

| Hardware | Platform |
| :--- | :--- |
| **Central Agent** | ESP32-S3 Board |
| **LED Agent** | ESP32 Board |
| **Sonic Agent**| ESP8266 NodeMCU |

## How to Get Started

This project is developed using **PlatformIO** with the Arduino framework.

1.  Clone this repository.
2.  Open the desired agent's folder (e.g., `central_agent/`) in VS Code with the PlatformIO extension.
3.  Connect your hardware and use the PlatformIO functions to **Build** and **Upload**.
4.  To monitor the output, use the **Serial Monitor** at a baud rate of **115200**.

---