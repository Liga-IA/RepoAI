# Agent Profile: The Central Agent

## 1. Role and Responsibilities

The **Central Agent** acts as the primary sensor hub and a cooperative coordinator within the multi-agent system. Its main purpose is to gather comprehensive information about its immediate environment, make decisions based on that information, and collaborate with other agents to achieve its goals.

Its key responsibilities are:
*   **Environmental Sensing**: Continuously monitors light levels, multiple temperature sources, humidity, and an analog input (potentiometer).
*   **Proactive Cooperation**: When it detects a specific state (like darkness), it actively seeks out and requests assistance from other agents (e.g., asking an LED agent to turn on).
*   **Reactive Services**: It listens for requests from other agents and provides services based on its own capabilities, such as sounding an alarm buzzer when requested by a sensor agent.
*   **Goal-Oriented Behavior**: It can adopt and pursue persistent goals, such as attempting to "cool down a room," which involves a continuous loop of actions until a success condition is met.

---

## 2. Hardware Profile

This agent is built on an **ESP32 Dev Board** and utilizes a rich set of peripherals.

| Component | Pin | Type | Status |
| :--- | :---: | :---: | :--- |
| LDR (Light Sensor) | GPIO 2 | Sensor | Active |
| Potentiometer | GPIO 1 | Sensor | Active |
| LM35 (Analog Temp) | GPIO 3 | Sensor | Active |
| DHT11 (Digital Temp/Humid)| GPIO 6 | Sensor | Active |
| Buzzer | GPIO 7 | Actuator| Active |
| IR Receiver | GPIO 8 | Sensor | Disabled in Code |

---

## 3. Network Capabilities

The Central Agent broadcasts the following capabilities to the network, allowing other agents to understand its role:

*   `CAP_SENSOR_LIGHT`: It can perceive and report on ambient light levels.
*   `CAP_SENSOR_POT`: It can read an analog input, often used to simulate user interaction.
*   `CAP_SENSOR_TEMP_ANALOG`: It can measure temperature via its LM35 sensor.
*   `CAP_SENSOR_TEMP_HUMID`: It can measure temperature and humidity via its DHT11 sensor.
*   `CAP_ACTUATOR_BUZZER`: It is capable of sounding an alarm and **listens for requests** from other agents to do so.

---

## 4. BDI Implementation (AgentSpeak)

The agent's decision-making logic is defined by a set of beliefs and plans. The C++ code implements a logic that can be represented in the AgentSpeak planning language as follows:

### Beliefs

The agent's "mind" or `BeliefBase` is populated by the following beliefs, which are added or removed based on sensor readings and network messages:

*   `low_light`: The ambient light is below the defined threshold.
*   `alarm_request_received`: A network message has been received requesting the buzzer to sound.
*   `neighbor(led_actuator)`: An agent with LED actuator capabilities has been discovered on the network.
*   `has_capability(led, on_off)`: Confirms the discovered neighbor can be turned on and off.
*   `is_hot`: The temperature from either the LM35 or DHT11 sensor is above the threshold (28°C).
*   `is_humid`: The humidity from the DHT11 is above the threshold (70%).
*   `pot_is_high`: The potentiometer's value is above the defined threshold, often simulating a user turning a dial to "high."

### Plans

These are the rules that trigger the agent's actions.

```agentspeak
// Plan 1: At startup, announce readiness.
+!start <- .show_ready_message.

// --- Proactive Cooperation Plans ---

// Plan 2: If it gets dark AND an LED agent is available, request it to turn on.
+low_light : neighbor(led_actuator) & has_capability(led, on_off)
    <- .request_cooperation_on.

// Plan 3: If it becomes light again AND an LED agent is available, request it to turn off.
-low_light : neighbor(led_actuator) & has_capability(led, on_off)
    <- .request_cooperation_off.

// --- Reactive Service Plan ---

// Plan 4: If a request to sound the alarm is received, sound the buzzer.
// The belief is immediately removed to prevent the alarm from looping indefinitely from a single request.
+alarm_request_received
    <- .sound_buzzer;
       -alarm_request_received.

// --- Goal-Oriented Behavior Plans (Simulated Air Conditioner) ---

// Plan 5: When the room becomes hot, the agent adopts the GOAL of cooling it down.
+is_hot
    <- +!cool_down_room. // Add intention to cool the room

// Plan 6 (The Looping Plan): If the agent intends to cool the room, BUT the user
// has NOT turned the dial up (pot_is_high is false), sound an intermittent alarm
// and re-post the goal to try again in the next cycle.
+!cool_down_room : not pot_is_high
    <- .sound_buzzer;
       +!cool_down_room. // Re-add the intention, creating a loop

// Plan 7 (The Exit Plan): If the agent intends to cool the room AND the user
// HAS turned the dial up (pot_is_high is true), the goal is achieved. Stop the process.
+!cool_down_room : pot_is_high
    <- .print("Goal achieved: Room is being cooled.");
       -is_hot. // Remove the initial trigger
```

---

## 5. Code Breakdown

*   **`setup()`**: Initializes hardware pins, serial communication, and the ESP-NOW manager. It constructs the agent's capability bitmask and starts the network discovery process.
*   **`loop()`**: The main execution cycle is managed by non-blocking timers (`millis()`). It handles four distinct tasks in a round-robin fashion:
    1.  **Sensor Reading**: Periodically reads all connected sensors (LDR, POT, LM35, DHT11) and generates BDI events (`+belief` or `-belief`) if their state changes.
    2.  **Network Tasks**: Sends out discovery broadcasts at a regular interval and cleans up disconnected neighbors.
    3.  **Belief Synchronization**: Checks the status of the neighbor table and updates the agent's internal beliefs about available partners (e.g., adding `neighbor(led_actuator)` when one is found).
    4.  **BDI Deliberation**: Calls `agent.run()`, which executes one cycle of the BDI reasoning loop (perceive events, update beliefs, select and execute plans).
*   **`on_message_received()`**: This callback function is the entry point for all network communication. It processes discovery messages to update the neighbor table and handles incoming cooperation requests, translating them into BDI events for the agent to process.
*   **`action_*()` functions**: These are the "hands" of the agent. Each function (e.g., `action_sound_buzzer`, `action_request_cooperation_on`) corresponds to an action that can be called from within a BDI plan.

---

## 6. How to Use

1.  Open the `central-agent` project folder in Visual Studio Code with the PlatformIO extension.
2.  Ensure the `platformio.ini` file is configured for your specific ESP32 board.
3.  Connect the hardware as defined in the pinout table.
4.  Use the PlatformIO interface to **Build** and **Upload** the code.
5.  Open the **Serial Monitor** at a baud rate of **115200** to view the agent's status, sensor readings, and decision-making logs.