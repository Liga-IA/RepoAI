# Agent Profile: The Sonic Agent

## 1. Role and Responsibilities

The **Sonic Agent** is a highly specialized **sensor agent**, built on a powerful and flexible platform (ESP32-S3). Its sole purpose is to monitor a specific physical area for obstacles using an ultrasonic sensor. It is a proactive agent, meaning it initiates cooperation rather than waiting for requests.

Its key responsibilities are:
*   **Proximity Detection**: To frequently measure the distance to the nearest object in its line of sight.
*   **State Change Reporting**: It doesn't just report danger; it intelligently reports the *change* in state. It sends one type of request when an obstacle is first detected and another when the area is subsequently cleared.
*   **Initiating Cooperation**: Upon detecting an obstacle, it searches the network for an agent capable of sounding an alarm (`CAP_ACTUATOR_BUZZER`) and sends it a direct request to act.
*   **Network Presence**: It continuously broadcasts its own capability (`CAP_SENSOR_ULTRASONIC`) so other agents are aware of its function, even if they don't currently use it.

---

## 2. Hardware Profile

This agent is built on an **ESP32-S3 Board**, demonstrating the system's flexibility across different hardware platforms. Its hardware is minimal and focused on its specific task.

| Component | Pin | Type | Status |
| :--- | :---: | :---: | :--- |
| HC-SR04 Trig Pin | GPIO 5 | Sensor | Active |
| HC-SR04 Echo Pin | GPIO 4 | Sensor | Active |

---

## 3. Network Capabilities

The Sonic Agent broadcasts a single, highly specific capability to the network:

*   `CAP_SENSOR_ULTRASONIC`: This announces that the agent can detect object proximity and will proactively send cooperation requests based on its sensor readings.

---

## 4. BDI Implementation (AgentSpeak)

The agent's logic is proactive and event-driven, focused on translating physical perception into network-wide actions.

### Beliefs

The agent's `BeliefBase` contains one primary sensory belief:

*   `obstacle_detected`: Added when an object is measured within the `OBSTACLE_THRESHOLD_CM` (10 cm) and removed when the object is no longer present.

### Plans

The agent's plans are triggered by the addition or removal of its core belief.

```agentspeak
// Plan 1: At startup, announce readiness.
+!start <- .show_ready_message.

// Plan 2: When an obstacle is newly detected, find an agent
// with a buzzer and request it to sound an alarm.
+obstacle_detected
    <- .request_cooperation_alarm.

// Plan 3: When an obstacle is no longer detected (the area is clear),
// find an agent with a buzzer and request it to stop the alarm.
-obstacle_detected
    <- .report_area_clear.
```

---

## 5. Code Breakdown

*   **`setup()`**: Initializes the HC-SR04 sensor pins and starts the ESP-NOW manager. It identifies itself as "SonicAgent" and broadcasts its `CAP_SENSOR_ULTRASONIC` capability.
*   **`loop()`**: The main loop is optimized for responsiveness.
    1.  **Sensor Check**: Calls `check_sonic_sensor()` frequently (every 200ms) to ensure low-latency obstacle detection.
    2.  **Network Maintenance**: Handles the periodic sending of discovery broadcasts and the cleanup of stale neighbors.
    3.  **BDI Deliberation**: Executes the `agent.run()` cycle to process any new events (like `+obstacle_detected`) and trigger the appropriate plans.
*   **`check_sonic_sensor()`**: This is the agent's perception function. It triggers the ultrasonic sensor, measures the echo duration, and calculates the distance. Crucially, it only generates a BDI event when the state *changes* (from clear to obstacle, or vice-versa) to prevent spamming the network with redundant requests.
*   **`on_message_received()`**: This callback handles incoming network packets. For this agent, it's primarily used to process `MSG_DISCOVERY` packets to build its internal table of neighbors and their capabilities. It also acknowledges cooperation responses but does not act on incoming requests.
*   **`action_*()` functions**: These are the agent's hands.
    *   `action_request_cooperation_alarm()`: Searches its neighbor table for an agent with `CAP_ACTUATOR_BUZZER` and sends it a cooperation request with `action_type = 3`.
    *   `action_report_area_clear()`: Performs the same search and sends a request with `action_type = 4` to signal that the threat has passed.

---

## 6. How to Use

1.  Open the `sonic-agent` project folder in Visual Studio Code with the PlatformIO extension.
2.  Ensure the `platformio.ini` file is configured for your specific **ESP32-S3 board**.
3.  Connect the HC-SR04 sensor as defined in the pinout table (Trig to GPIO5, Echo to GPIO4).
4.  Use the PlatformIO interface to **Build** and **Upload** the code.
5.  Open the **Serial Monitor** at a baud rate of **115200** to see live distance readings and logs of cooperation requests.