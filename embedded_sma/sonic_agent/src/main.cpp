#include <Arduino.h>
#include "agent.h"
#include "configuration.h"
#include "functions.h"
#include "espnow_manager.h"

// --- Hardware Setup ---
const int TRIG_PIN = 5; // GPIO 5
const int ECHO_PIN = 4; // GPIO 4
const int OBSTACLE_THRESHOLD_CM = 10; // Detection threshold

// --- Global Variables ---
AgentSettings settings;
Agent agent(
    settings.get_belief_base(),
    settings.get_event_base(),
    settings.get_plan_base(),
    settings.get_intention_base()
);
ESPNowManager espnow_manager;
bool obstacle_was_detected = false; // Previous sensor state

// Manual Timers
unsigned long last_discovery_time = 0;
unsigned long last_cleanup_time = 0;
unsigned long last_sensor_check_time = 0;
unsigned long last_print_time = 0;

// --- Hardware and Action Functions ---
void setup_hardware() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  digitalWrite(TRIG_PIN, LOW);
  Serial.println("[SETUP] Hardware (HC-SR04 Sensor) initialized.");
}

bool action_show_ready_message() {
  Serial.println("[ACTION] SONIC Agent ready for operation.");
  return true;
}

bool action_request_cooperation_alarm() {
  Serial.println("[ACTION] Obstacle detected! Looking for agent with BUZZER to cooperate...");
  NeighborEntry_t buzzer_agent;
  if (espnow_manager.find_neighbor_by_capability(CAP_ACTUATOR_BUZZER, &buzzer_agent)) {
    Serial.printf("[COOPERATION] Agent with buzzer found. Sending request to %02X:%02X...\n", buzzer_agent.mac[0], buzzer_agent.mac[1]);
    CooperationAction_t action_to_send;
    action_to_send.action_type = 3; // 3 = SOUND ALARM (convention)
    action_to_send.priority = 1;
    return espnow_manager.send_cooperation_request(buzzer_agent.mac, &action_to_send);
  } else {
    Serial.println("[COOPERATION] No agent with buzzer found.");
    return false;
  }
}

bool action_report_area_clear() {
  Serial.println("[ACTION] Area clear. Notifying actuator to stop alarm.");
  NeighborEntry_t buzzer_agent;
  if (espnow_manager.find_neighbor_by_capability(CAP_ACTUATOR_BUZZER, &buzzer_agent)) {
    CooperationAction_t action_to_send;
    action_to_send.action_type = 4; // 4 = STOP ALARM (convention)
    action_to_send.priority = 1;
    return espnow_manager.send_cooperation_request(buzzer_agent.mac, &action_to_send);
  } else {
    return false;
  }
}

// --- Perception Function (Sensor) ---
void check_sonic_sensor() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 50000); // 50ms timeout
  int distance = duration * 0.034 / 2;

  bool obstacle_is_detected = (duration > 0 && distance < OBSTACLE_THRESHOLD_CM);

  if (obstacle_is_detected && !obstacle_was_detected) {
    Serial.printf("[SENSOR] Obstacle detected at %d cm. Generating BDI event.\n", distance);
    settings.get_event_base()->add_event(Event(EventOperator::BELIEF_ADDITION, Proposition(3)));
    obstacle_was_detected = true;
  } else if (!obstacle_is_detected && obstacle_was_detected) {
    Serial.println("[SENSOR] Area clear. Generating BDI event.");
    settings.get_event_base()->add_event(Event(EventOperator::BELIEF_DELETION, Proposition(3)));
    obstacle_was_detected = false;
  }
}

// --- ESP-NOW Callback ---
void on_message_received(const uint8_t* mac_addr, const uint8_t* data, int len) {
    NetworkMessage_t msg;
    if (len > sizeof(NetworkMessage_t)) return;
    memcpy(&msg, data, len);
    if (memcmp(msg.sender_mac, espnow_manager.get_agent_mac(), 6) == 0) return;
    
    if (msg.type == MSG_DISCOVERY) {
        espnow_manager.add_or_update_neighbor(msg.sender_mac, msg.payload[0]);
    } else if (msg.type == MSG_COOPERATION_RESPONSE) {
        Serial.printf("[NETWORK] Cooperation response received from %02X:%02X...\n", mac_addr[0], mac_addr[1]);
    }
}

// --- Setup ---
void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n=== Starting SONIC Agent (Sensor) ===");
  setup_hardware();
  
  if (!espnow_manager.initialize("SonicAgent", CAP_SENSOR_ULTRASONIC, on_message_received)) {
    Serial.println("Failed to initialize ESP-NOW. Restarting in 5s...");
    delay(5000);
    ESP.restart();
  }

  espnow_manager.start();
  Serial.println("=== System started successfully! ===");
}

// --- Main Loop ---
void loop() {
  unsigned long current_time = millis();

  if (current_time - last_sensor_check_time > 200) { // Check sensor 5x per second
    last_sensor_check_time = current_time;
    check_sonic_sensor();
  }

  if (current_time - last_discovery_time > DISCOVERY_INTERVAL_MS) {
    last_discovery_time = current_time;
    espnow_manager.send_discovery_broadcast();
  }

  if (current_time - last_cleanup_time > NEIGHBOR_TIMEOUT_MS) {
    last_cleanup_time = current_time;
    espnow_manager.cleanup_neighbors();
  }

  if (current_time - last_print_time > 10000) {
    last_print_time = current_time;
    espnow_manager.print_neighbor_table();
  }

  agent.run();
  delay(50);
}