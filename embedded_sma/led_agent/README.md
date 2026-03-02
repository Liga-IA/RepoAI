# Agent Profile: The LED Agent

## 1. Role and Responsibilities

The **LED Agent** is a specialized **actuator agent**. It is designed to be a simple, reliable, and responsive component in the network. Unlike sensor agents, it does not proactively perceive the environment; instead, its primary function is to listen for requests from other agents and perform a specific physical action.

Its key responsibilities are:
*   **Provide a Service**: Its main purpose is to offer an "illumination service" to any agent on the network that requests it.
*   **Reactive Behavior**: It remains idle until a valid cooperation request is received, at which point it executes its plan.
*   **Network Presence**: It regularly broadcasts its identity and capability (`CAP_ACTUATOR_LED`) so that other agents know it is available to help.
*   **Acknowledge Commands**: After successfully turning on its LED, it sends a confirmation response back to the original requester, closing the communication loop.

---

## 2. Hardware Profile

This agent is built on an **ESP32-S3 Board** (or any compatible ESP32/ESP8266) with a minimal hardware setup, reflecting its focused role.

| Component | Pin | Type | Status |
| :--- | :---: | :---: | :--- |
| LED | GPIO 15 | Actuator| Active |

---

## 3. Network Capabilities

The LED Agent broadcasts a single, clear capability to the network:

*   `CAP_ACTUATOR_LED`: This announces that the agent controls a physical LED and is actively listening for network commands to turn it on or off.

---

## 4. BDI Implementation (AgentSpeak)

The agent's logic is purely reactive, designed to translate network requests into physical actions. This logic can be represented in AgentSpeak as follows:

### Beliefs

The agent's `BeliefBase` is updated based on incoming network messages:

*   `turn_on_request_received`: A network message with `action_type = 1` has been received. This belief triggers the plan to turn the LED on.
*   `turn_off_request_received`: A network message with `action_type = 2` has been received. This belief triggers the plan to turn the LED off.

### Plans

These are the simple, direct rules that govern the agent's behavior.

```agentspeak
// Plan 1: At startup, announce readiness.
+!start <- .show_ready_message.

// Plan 2: When a request to turn on the LED is received,
// turn on the physical LED, send a confirmation back to the requester,
// and then remove the belief to complete the action.
+turn_on_request_received
    <- .led_on;
       .send_cooperation_response;
       -turn_on_request_received.

// Plan 3: When a request to turn off the LED is received,
// turn off the physical LED and remove the belief.
+turn_off_request_received
    <- .led_off;
       -turn_off_request_received.
```

---

## 5. Code Breakdown

*   **`setup()`**: Initializes the LED pin as an output and starts the ESP-NOW manager. It gives itself the name "LEDAgent" and broadcasts its `CAP_ACTUATOR_LED` capability.
*   **`loop()`**: The main loop is lean and efficient. It has three responsibilities:
    1.  **Network Maintenance**: Periodically sends discovery broadcasts and cleans up the neighbor table.
    2.  **BDI Deliberation**: Calls `agent.run()` to execute one cycle of the BDI reasoning loop.
    3.  **Logging**: Prints the neighbor table every 10 seconds for debugging.
*   **`on_message_received()`**: This is the agent's "ears." It listens for `MSG_COOPERATION_REQUEST` packets. When a valid request is received, it does not act directly; instead, it translates the request into a BDI **event** (e.g., `+turn_on_request_received`). This decouples the network logic from the decision-making logic. It also crucially saves the MAC address of the requester to know where to send the confirmation.
*   **`action_*()` functions**: These are the agent's "muscles."
    *   `action_led_on()` / `action_led_off()`: Directly control the state of the GPIO pin connected to the LED.
    *   `action_send_cooperation_response()`: Sends a confirmation packet back to the original requester using the saved MAC address.

---

## 6. How to Use

1.  Open the `led-agent` project folder in Visual Studio Code with the PlatformIO extension.
2.  Ensure the `platformio.ini` file is configured for your specific ESP32/ESP8266 board.
3.  Connect the hardware as defined in the pinout table.
4.  Use the PlatformIO interface to **Build** and **Upload** the code.
5.  Open the **Serial Monitor** at a baud rate of **115200** to view the agent's status and logs of received requests.